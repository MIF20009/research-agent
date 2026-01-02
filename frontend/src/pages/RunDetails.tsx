import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useRun, useRunArtifacts, useExecuteRun } from '../hooks/useApi';
import { Card, CardHeader, CardTitle, CardContent, Button, Badge, Skeleton } from '../components/ui';
import { formatDate, getStatusColor, copyToClipboard, downloadAsFile } from '../utils';
import { Play, Copy, Download, ArrowLeft, CheckCircle, Clock, AlertCircle, AlertTriangle, Info } from 'lucide-react';
import type { Artifact } from '../types';

interface Hypothesis {
  title: string;
  rationale: string;
  validation: string;
}

const STEPS = [
  { id: 'retrieve', label: 'Retrieve', description: 'Gathering relevant papers and data' },
  { id: 'extract', label: 'Extract', description: 'Extracting key information' },
  { id: 'synthesize', label: 'Synthesize', description: 'Creating comprehensive synthesis' },
  { id: 'gap_analysis', label: 'Gap Analysis', description: 'Identifying research gaps' },
  { id: 'hypotheses', label: 'Hypotheses', description: 'Generating research hypotheses' },
];

const STEP_DURATIONS = [4, 5, 6, 5, Infinity]; // seconds for visual progression, Infinity for hypotheses (hold until backend completes)

const getCurrentStepIndex = (elapsedSeconds: number, artifacts: Artifact[], runStatus: string): number => {
  if (runStatus === 'completed') {
    return 4; // All steps completed
  }

  if (elapsedSeconds <= 0) {
    return 0; // Not started
  }

  // Time-based progression for first 4 steps (up to gap analysis)
  let currentIndex = 0;
  let cumulativeTime = 0;

  for (let i = 0; i < 4; i++) {
    cumulativeTime += STEP_DURATIONS[i];
    if (elapsedSeconds >= cumulativeTime) {
      currentIndex = i + 1;
    } else {
      break;
    }
  }

  // Backend-aware overrides: advance if artifacts are available for later steps
  const hasSynthesis = artifacts.some(a => a.kind.toLowerCase().includes('synthesis'));
  const hasGaps = artifacts.some(a => a.kind.toLowerCase().includes('gaps'));
  const hasHypotheses = artifacts.some(a => a.kind.toLowerCase().includes('hypotheses'));

  if (hasSynthesis) {
    currentIndex = Math.max(currentIndex, 3); // At least gap analysis running
  }
  if (hasGaps) {
    currentIndex = Math.max(currentIndex, 4); // At least hypotheses running
  }
  if (hasHypotheses) {
    currentIndex = Math.max(currentIndex, 4); // Hypotheses running
  }

  return Math.min(currentIndex, 4); // Cap at hypotheses
};

const getStepStatus = (stepIndex: number, currentStepIndex: number, runStatus: string): 'completed' | 'running' | 'pending' | 'failed' => {
  if (runStatus === 'failed') return 'failed';
  if (runStatus === 'completed') return 'completed';

  if (stepIndex < currentStepIndex) return 'completed';
  if (stepIndex === currentStepIndex) return 'running';
  return 'pending';
};

const getConnectorClass = (stepIndex: number, currentStepIndex: number, runStatus: string): string => {
  if (runStatus === 'completed') return 'bg-green-500';
  if (runStatus === 'failed') return 'bg-red-400';

  if (stepIndex < currentStepIndex - 1) return 'bg-green-500'; // Previous connectors green
  if (stepIndex === currentStepIndex - 1) return 'bg-blue-500 animate-pulse'; // Between completed and running: blue animated
  return 'bg-gray-300'; // Future connectors gray
};

const ArtifactRenderer: React.FC<{ artifact: Artifact }> = ({ artifact }) => {
  const renderContent = () => {
    switch (artifact.kind.toLowerCase()) {
      case 'synthesis':
        return (
          <div className="prose prose-sm max-w-none">
            {artifact.content.split('\n').map((paragraph: string, i: number) => (
              <p key={i} className="mb-4">{paragraph}</p>
            ))}
          </div>
        );
      case 'gaps':
        return (
          <ul className="space-y-2">
            {artifact.content.split('\n').filter((line: string) => line.trim()).map((gap: string, i: number) => (
              <li key={i} className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>{gap}</span>
              </li>
            ))}
          </ul>
        );
      case 'hypotheses':
        try {
          const hypotheses = JSON.parse(artifact.content) as Hypothesis[];
          return (
            <div className="space-y-6">
              {hypotheses.map((hypothesis: Hypothesis, i: number) => (
                <Card key={i} className="border-l-4 border-l-blue-500">
                  <CardContent className="pt-4">
                    <h4 className="font-semibold text-lg mb-3 text-blue-900">{hypothesis.title}</h4>
                    <div className="space-y-3">
                      <div>
                        <h5 className="font-medium text-gray-800 mb-1">Rationale:</h5>
                        <p className="text-gray-700 leading-relaxed">{hypothesis.rationale}</p>
                      </div>
                      <div>
                        <h5 className="font-medium text-gray-800 mb-1">Validation:</h5>
                        <p className="text-gray-700 leading-relaxed">{hypothesis.validation}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          );
        } catch {
          // Handle formatted text (fallback for non-JSON format)
          const content = artifact.content;
          const hypothesisBlocks = content.split(/(?=Hypothesis \d+:)/).filter(block => block.trim());

          return (
            <div className="space-y-6">
              {hypothesisBlocks.map((block: string, i: number) => {
                const lines = block.trim().split('\n').filter(line => line.trim());
                const title = lines[0] || `Hypothesis ${i + 1}`;

                // Extract rationale and validation sections
                const rationaleStart = lines.findIndex(line => line.toLowerCase().includes('rationale:'));
                const validationStart = lines.findIndex(line => line.toLowerCase().includes('validation:'));

                const rationale = rationaleStart !== -1
                  ? lines.slice(rationaleStart + 1, validationStart !== -1 ? validationStart : undefined).join(' ').trim()
                  : '';

                const validation = validationStart !== -1
                  ? lines.slice(validationStart + 1).join(' ').trim()
                  : '';

                return (
                  <Card key={i} className="border-l-4 border-l-blue-500">
                    <CardContent className="pt-4">
                      <h4 className="font-semibold text-lg mb-3 text-blue-900">{title}</h4>
                      <div className="space-y-3">
                        {rationale && (
                          <div>
                            <h5 className="font-medium text-gray-800 mb-1">Rationale:</h5>
                            <p className="text-gray-700 leading-relaxed">{rationale}</p>
                          </div>
                        )}
                        {validation && (
                          <div>
                            <h5 className="font-medium text-gray-800 mb-1">Validation:</h5>
                            <p className="text-gray-700 leading-relaxed">{validation}</p>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          );
        }
      default:
        return <p>{artifact.content}</p>;
    }
  };

  return renderContent();
};

export const RunDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const runId = id ? parseInt(id, 10) : undefined;
  const [activeTab, setActiveTab] = useState('synthesis');
  const [showExecuteConfirm, setShowExecuteConfirm] = useState(false);
  const [executionStartTime, setExecutionStartTime] = useState<number | null>(null);
  const [tick, setTick] = useState(0); // Force re-renders for animations

  const { data: run, isLoading: runLoading, error: runError } = useRun(runId);
  const { data: artifacts, isLoading: artifactsLoading } = useRunArtifacts(runId);
  const executeRunMutation = useExecuteRun();

  // Refresh-safe execution start time using localStorage
  const storageKey = runId ? `executionStartTime_${runId}` : null;

  useEffect(() => {
    if (run?.status === 'running' && storageKey) {
      const stored = localStorage.getItem(storageKey);
      if (stored && !executionStartTime) {
        setExecutionStartTime(parseInt(stored));
      } else if (!executionStartTime) {
        const now = Date.now();
        setExecutionStartTime(now);
        localStorage.setItem(storageKey, now.toString());
      }
    } else if (run?.status !== 'running' && storageKey) {
      localStorage.removeItem(storageKey);
    }
  }, [run?.status, executionStartTime, storageKey]);

  // Force re-renders every second while running for smooth animations
  useEffect(() => {
    if (run?.status === 'running') {
      const interval = setInterval(() => {
        setTick(prev => prev + 1);
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [run?.status]);

  const elapsedSeconds = executionStartTime ? (Date.now() - executionStartTime) / 1000 : 0;
  // Use tick to force re-renders for smooth animations
  const currentElapsed = tick ? elapsedSeconds : elapsedSeconds;
  const currentStepIndex = getCurrentStepIndex(currentElapsed, artifacts || [], run?.status || 'created');
  const currentStep = STEPS[currentStepIndex];

  if (runError) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-red-600 mb-4">Failed to load run: {runError.message}</p>
            <Link to="/">
              <Button variant="outline">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const handleExecute = () => {
    setShowExecuteConfirm(true);
  };

  const confirmExecute = () => {
    const now = Date.now();
    setExecutionStartTime(now);
    if (storageKey) {
      localStorage.setItem(storageKey, now.toString());
    }
    if (runId) {
      executeRunMutation.mutate(runId);
      setShowExecuteConfirm(false);
    }
  };

  const handleCopy = async (content: string) => {
    const success = await copyToClipboard(content);
    if (success) {
      // Could add toast here
    }
  };

  const handleExport = (content: string, filename: string) => {
    downloadAsFile(content, filename);
  };

  const filteredArtifacts = artifacts?.filter(a => a.kind.toLowerCase().includes(activeTab)) || [];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <Link to="/" className="inline-flex items-center text-blue-600 hover:text-blue-800">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Link>
        </div>

        {runLoading ? (
          <Card>
            <CardHeader>
              <Skeleton className="h-8 w-1/2" />
              <Skeleton className="h-4 w-1/4" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-32 w-full" />
            </CardContent>
          </Card>
        ) : run ? (
          <>
            <Card className="mb-6">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-2xl">{run.topic}</CardTitle>
                    <p className="text-gray-600 mt-1">Created: {formatDate(run.created_at)}</p>
                  </div>
                  <Badge className={getStatusColor(run.status)}>{run.status}</Badge>
                </div>
              </CardHeader>
              <CardContent>
                {run.status === 'running' && (
                  <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="animate-spin rounded-full h-6 w-6 border-2 border-blue-600 border-t-transparent"></div>
                      <div>
                        <p className="text-sm font-medium text-blue-900">
                          Research Process Active
                        </p>
                        <p className="text-xs text-blue-700 mt-1">
                          Currently processing: {currentStep?.label || 'Research'} (~20-30s total)
                        </p>
                        <div className="mt-2 w-full bg-blue-200 rounded-full h-2">
                          <div
                            className="bg-blue-600 h-2 rounded-full transition-all duration-1000 ease-out"
                            style={{
                              width: (() => {
                                const totalVisualTime = 4 + 5 + 6 + 5; // 20 seconds for 90% progress
                                const progress = Math.min((elapsedSeconds / totalVisualTime) * 90, 90);
                                return `${progress}%`;
                              })()
                            }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                <div className="flex justify-between items-center">
                  <div className="flex space-x-4">
                    {STEPS.map((step, index) => {
                      const status = getStepStatus(index, currentStepIndex, run.status);
                      return (
                        <div key={step.id} className="flex items-center space-x-2">
                          {status === 'completed' && <CheckCircle className="h-5 w-5 text-green-500" />}
                          {status === 'running' && <Clock className="h-5 w-5 text-blue-500 animate-pulse" />}
                          {status === 'failed' && <AlertTriangle className="h-5 w-5 text-red-500" />}
                          {status === 'pending' && <AlertCircle className="h-5 w-5 text-gray-400" />}
                          <div>
                            <p className={`text-sm font-medium ${
                              status === 'completed' ? 'text-green-700' :
                              status === 'running' ? 'text-blue-700' :
                              status === 'failed' ? 'text-red-700' :
                              'text-gray-500'
                            }`}>
                              {step.label}
                            </p>
                            <p className="text-xs text-gray-500">{step.description}</p>
                          </div>
                          {index < STEPS.length - 1 && <div className={`w-8 h-px ${getConnectorClass(index, currentStepIndex, run.status)}`} />}
                        </div>
                      );
                    })}
                  </div>
                  {run.status === 'created' && (
                    <Button onClick={handleExecute} disabled={executeRunMutation.isPending}>
                      <Play className="h-4 w-4 mr-2" />
                      Start Research Process
                    </Button>
                  )}
                  {run.status === 'running' && (
                    <div className="flex items-center space-x-2 text-blue-600 bg-blue-50 px-3 py-2 rounded-lg">
                      <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-600 border-t-transparent"></div>
                      <span className="text-sm font-medium">
                        Processing: {currentStep?.label || 'Research'}
                      </span>
                    </div>
                  )}
                  {run.status === 'completed' && (
                    <div className="flex items-center space-x-2 text-green-600 bg-green-50 px-3 py-2 rounded-lg">
                      <CheckCircle className="h-4 w-4" />
                      <span className="text-sm font-medium">Research completed</span>
                    </div>
                  )}
                  {run.status === 'failed' && (
                    <div className="flex items-center space-x-2 text-red-600 bg-red-50 px-3 py-2 rounded-lg">
                      <AlertTriangle className="h-4 w-4" />
                      <span className="text-sm font-medium">Research failed</span>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Execution Confirmation Dialog */}
            {showExecuteConfirm && (
              <Card className="mb-6 border-blue-200 bg-blue-50">
                <CardContent className="pt-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3">
                      <Info className="h-5 w-5 text-blue-600 mt-0.5" />
                      <div>
                        <p className="font-medium text-blue-900 mb-1">Ready to start the research process?</p>
                        <p className="text-blue-700 text-sm">
                          This will initiate the multi-agent research workflow: retrieve → extract → synthesize → gap analysis → hypotheses generation.
                          The process may take several minutes to complete.
                        </p>
                      </div>
                    </div>
                    <div className="flex space-x-2 ml-4">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setShowExecuteConfirm(false)}
                        disabled={executeRunMutation.isPending}
                      >
                        Cancel
                      </Button>
                      <Button
                        size="sm"
                        onClick={confirmExecute}
                        loading={executeRunMutation.isPending}
                      >
                        Start Research
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Status Information */}
            {run.status === 'created' && !showExecuteConfirm && (
              <Card className="mb-6 border-amber-200 bg-amber-50">
                <CardContent className="pt-4">
                  <div className="flex items-start space-x-3">
                    <AlertCircle className="h-5 w-5 text-amber-600 mt-0.5" />
                    <div>
                      <p className="font-medium text-amber-900">Next Step</p>
                      <p className="text-amber-700 text-sm mt-1">
                        Click "Start Research Process" to begin the automated research workflow.
                        The system will gather relevant papers, extract key information, create synthesis, identify gaps, and generate hypotheses.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Success Message */}
            {run.status === 'completed' && artifacts && artifacts.length > 0 && (
              <Card className="mb-6 border-green-200 bg-gradient-to-r from-green-50 to-emerald-50">
                <CardContent className="pt-4">
                  <div className="flex items-start space-x-3">
                    <CheckCircle className="h-6 w-6 text-green-600 mt-0.5" />
                    <div>
                      <p className="font-medium text-green-900">Research Complete!</p>
                      <p className="text-green-700 text-sm mt-1">
                        The multi-agent research process has finished successfully.
                        Review the comprehensive analysis, gap identification, and generated hypotheses below.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            <Card>
              <CardHeader>
                <CardTitle>Artifacts</CardTitle>
                <div className="flex space-x-4 mt-4">
                  {['synthesis', 'gaps', 'hypotheses'].map((tab) => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab)}
                      className={`px-4 py-2 rounded-md text-sm font-medium ${
                        activeTab === tab
                          ? 'bg-blue-100 text-blue-700'
                          : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      {tab.charAt(0).toUpperCase() + tab.slice(1)}
                    </button>
                  ))}
                </div>
              </CardHeader>
              <CardContent>
                {artifactsLoading ? (
                  <Skeleton className="h-64 w-full" />
                ) : filteredArtifacts.length > 0 ? (
                  <div className="space-y-4">
                    <div className="flex justify-end space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleCopy(filteredArtifacts.map(a => a.content).join('\n\n'))}
                      >
                        <Copy className="h-4 w-4 mr-2" />
                        Copy
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleExport(
                          JSON.stringify(filteredArtifacts, null, 2),
                          `${run.topic.replace(/\s+/g, '_')}_${activeTab}.json`                        )}
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Export JSON
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleExport(
                          filteredArtifacts.map(a => a.content).join('\n\n'),
                          `${run.topic.replace(/\s+/g, '_')}_${activeTab}.txt`
                        )}
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Export TXT
                      </Button>
                    </div>
                    {filteredArtifacts.map((artifact) => (
                      <ArtifactRenderer key={artifact.id} artifact={artifact} />
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <AlertCircle className="mx-auto h-12 w-12 text-gray-400" />
                    <h3 className="mt-2 text-sm font-medium text-gray-900">
                      {run.status === 'created' ? 'Ready to start research' : 'No artifacts yet'}
                    </h3>
                    <p className="mt-1 text-sm text-gray-500">
                      {run.status === 'created'
                        ? 'Click "Start Research Process" above to begin the automated research workflow.'
                        : run.status === 'running'
                        ? 'The research agents are working. Artifacts will appear here as they complete each step.'
                        : 'Artifacts will appear here once the research process completes.'
                      }
                    </p>
                    {run.status === 'running' && (
                      <div className="mt-4 flex justify-center">
                        <div className="animate-pulse text-blue-600 text-sm">
                          Processing: {currentStep?.label || 'Research'}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </>
        ) : null}
      </div>
    </div>
  );
};