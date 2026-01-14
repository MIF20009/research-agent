import React from 'react';
import { Link } from 'react-router-dom';
import { useRuns } from '../hooks/useApi';
import { Card, CardHeader, CardTitle, CardContent, Button, Badge, Skeleton } from '../components/ui';
import { formatDate, getStatusColor } from '../utils';
import { Plus, ExternalLink, BookOpen } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const { data: runs, isLoading, error } = useRuns(10);

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-red-600 mb-4">Failed to load runs: {error.message}</p>
            <Button onClick={() => window.location.reload()}>Retry</Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600 mt-2">Manage your research runs</p>
          </div>
          <Link to="/new-run">
            <Button className="flex items-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>New Run</span>
            </Button>
          </Link>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {isLoading ? (
            Array.from({ length: 6 }).map((_, i) => (
              <Card key={i}>
                <CardHeader>
                  <Skeleton className="h-6 w-3/4" />
                  <Skeleton className="h-4 w-1/2" />
                </CardHeader>
                <CardContent>
                  <Skeleton className="h-4 w-full mb-2" />
                  <Skeleton className="h-4 w-2/3" />
                </CardContent>
              </Card>
            ))
          ) : runs && runs.length > 0 ? (
            runs.map((run) => (
              <Card key={run.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <CardTitle className="text-lg line-clamp-2">{run.topic}</CardTitle>
                    <Badge className={getStatusColor(run.status)}>{run.status}</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">
                    Created: {formatDate(run.created_at)}
                  </p>
                  <div className="mt-auto">
                    <Link to={`/runs/${run.id}`}>
                      <Button variant="outline" className="w-full flex items-center justify-center space-x-2">
                        <ExternalLink className="h-4 w-4" />
                        <span>Open</span>
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            <div className="col-span-full text-center py-12">
              <BookOpen className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No runs yet</h3>
              <p className="mt-1 text-sm text-gray-500">Get started by creating your first research run.</p>
              <div className="mt-6">
                <Link to="/new-run">
                  <Button>
                    <Plus className="h-4 w-4 mr-2" />
                    Create New Run
                  </Button>
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};