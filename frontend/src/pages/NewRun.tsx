import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCreateRun } from '../hooks/useApi';
import { Card, CardHeader, CardTitle, CardContent, Button, Input } from '../components/ui';
import { Lightbulb } from 'lucide-react';

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
  const navigate = useNavigate();
  const createRunMutation = useCreateRun();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!topic.trim()) {
      setError('Topic is required');
      return;
    }

    try {
      const newRun = await createRunMutation.mutateAsync({ topic: topic.trim() });
      navigate(`/runs/${newRun.id}`);
    } catch {
      // Error is handled by the mutation
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setTopic(suggestion);
    setError('');
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
                <p><strong>Step 2:</strong> Start the automated research process</p>
                <p><strong>Step 3:</strong> Multi-agent system will: retrieve papers → extract information → synthesize findings → identify gaps → generate hypotheses</p>
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

              <Button
                type="submit"
                className="w-full"
                loading={createRunMutation.isPending}
                disabled={!topic.trim()}
              >
                Create Run
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};