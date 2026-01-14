import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCreateRun } from '../hooks/useApi';
import { Card, CardHeader, CardTitle, CardContent, Button, Input } from '../components/ui';
import { Lightbulb, Upload, X } from 'lucide-react';
import { runsApi } from '../api/endpoints';

const TOPIC_SUGGESTIONS = [
  'LLMs for literature review',
  'AI in education',
  'Machine learning applications in healthcare',
  'Natural language processing advancements',
  'Computer vision in autonomous vehicles',
  'Blockchain technology in finance',
  'Quantum computing developments',
  'Sustainable energy solutions',
];

export const NewRun: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [error, setError] = useState('');
  const [uploadPapers, setUploadPapers] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  const createRunMutation = useCreateRun();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!topic.trim()) {
      setError('Topic is required');
      return;
    }

    if (uploadPapers && selectedFiles.length === 0) {
      setError('Please upload at least one paper');
      return;
    }

    try {
      const newRun = await createRunMutation.mutateAsync({
        topic: topic.trim(),
        upload_papers: uploadPapers,
      });

      // If user selected to upload papers, upload them now
      if (uploadPapers && selectedFiles.length > 0) {
        setUploading(true);
        try {
          await runsApi.uploadPapers(newRun.id, selectedFiles);
          navigate(`/runs/${newRun.id}`);
        } catch (uploadError) {
          setError(`Failed to upload papers: ${uploadError}`);
        } finally {
          setUploading(false);
        }
      } else {
        navigate(`/runs/${newRun.id}`);
      }
    } catch {
      // Error is handled by the mutation
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setTopic(suggestion);
    setError('');
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      const newFiles = Array.from(files);
      const totalFiles = selectedFiles.length + newFiles.length;

      if (totalFiles > 20) {
        setError(`Maximum 20 files allowed. You selected ${totalFiles} files.`);
        return;
      }

      const pdfFiles = newFiles.filter((file) => file.type === 'application/pdf');
      if (pdfFiles.length !== newFiles.length) {
        setError('Only PDF files are allowed');
        return;
      }

      setSelectedFiles([...selectedFiles, ...newFiles]);
      setError('');
    }
  };

  const removeFile = (index: number) => {
    setSelectedFiles(selectedFiles.filter((_, i) => i !== index));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Lightbulb className="h-6 w-6 text-blue-600" />
              <span>Create New Research Run</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h3 className="text-sm font-medium text-blue-900 mb-2">Research Process Overview</h3>
              <div className="text-sm text-blue-700 space-y-1">
                <p><strong>Step 1:</strong> Create a research run with your topic</p>
                <p><strong>Step 2:</strong> {uploadPapers ? 'Upload your papers (1-20 PDFs)' : 'Start the automated research process'}</p>
                <p><strong>Step 3:</strong> Multi-agent system will: {uploadPapers ? 'extract information → synthesize findings → identify gaps → generate hypotheses' : 'retrieve papers → extract information → synthesize findings → identify gaps → generate hypotheses'}</p>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
                  Research Topic
                </label>
                <Input
                  id="topic"
                  type="text"
                  placeholder="Enter your research topic..."
                  value={topic}
                  onChange={(e) => {
                    setTopic(e.target.value);
                    setError('');
                  }}
                  error={error}
                  className="w-full"
                />
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700 mb-3">Quick suggestions:</p>
                <div className="flex flex-wrap gap-2">
                  {TOPIC_SUGGESTIONS.map((suggestion) => (
                    <button
                      key={suggestion}
                      type="button"
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="px-3 py-1 text-sm bg-blue-50 text-blue-700 rounded-full hover:bg-blue-100 transition-colors"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <div className="flex items-center space-x-3">
                  <label htmlFor="upload-toggle" className="text-sm font-medium text-gray-700">
                    Upload papers instead of retrieving them
                  </label>
                  <button
                    type="button"
                    onClick={() => {
                      setUploadPapers(!uploadPapers);
                      setSelectedFiles([]);
                      setError('');
                    }}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      uploadPapers ? 'bg-blue-600' : 'bg-gray-300'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        uploadPapers ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              </div>

              {uploadPapers && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Upload PDF Papers (1-20 files)
                  </label>
                  <div
                    className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-600">
                      Click to upload or drag and drop PDF files
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      Maximum 20 PDFs, up to 50MB each
                    </p>
                  </div>
                  <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="hidden"
                  />

                  {selectedFiles.length > 0 && (
                    <div className="mt-4">
                      <p className="text-sm font-medium text-gray-700 mb-2">
                        Selected files ({selectedFiles.length}/20)
                      </p>
                      <div className="space-y-2">
                        {selectedFiles.map((file, index) => (
                          <div
                            key={index}
                            className="flex items-center justify-between bg-gray-50 p-2 rounded border border-gray-200"
                          >
                            <span className="text-sm text-gray-700 truncate">{file.name}</span>
                            <button
                              type="button"
                              onClick={() => removeFile(index)}
                              className="text-red-500 hover:text-red-700"
                            >
                              <X className="h-4 w-4" />
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
                  {error}
                </div>
              )}

              <Button
                type="submit"
                className="w-full"
                loading={createRunMutation.isPending || uploading}
                disabled={!topic.trim() || (uploadPapers && selectedFiles.length === 0)}
              >
                {uploading ? 'Uploading papers...' : 'Create Run'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};