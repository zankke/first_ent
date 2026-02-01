import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Button } from '../components/ui/button';
import { toast } from 'sonner';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);

  if (!authContext) {
    throw new Error('AuthContext must be used within an AuthProvider');
  }

  const { login } = authContext;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const { error } = await login(email, password);
      
      if (error) {
        toast.error(error.message || 'Login failed. Please check your credentials.');
      } else {
        toast.success('Login successful!');
        navigate('/'); // Redirect to dashboard or home page
      }
    } catch (err) {
      toast.error('An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <Card className="w-[500px] rounded-2xl shadow-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold text-foreground flex items-center justify-center gap-2">
            <span>
              <svg width="28" height="28" viewBox="0 0 20 20" fill="none" aria-hidden="true" className="inline-block text-primary" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 11.5a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z" fill="currentColor"/>
                <path fillRule="evenodd" clipRule="evenodd" d="M6.75 7V5.75A3.25 3.25 0 0 1 13.25 5.75V7h.5A1.75 1.75 0 0 1 15.5 8.75v5.5A1.75 1.75 0 0 1 13.75 16H6.25A1.75 1.75 0 0 1 4.5 14.25v-5.5A1.75 1.75 0 0 1 6.25 7h.5Zm1.5 0h3.5V5.75a1.75 1.75 0 1 0-3.5 0V7Zm5.5 1.75a.25.25 0 0 0-.25-.25h-9a.25.25 0 0 0-.25.25v5.5c0 .138.112.25.25.25h7.5c.138 0 .25-.112.25-.25v-5.5Z" fill="currentColor"/>
              </svg>
            </span>
            <span>TAMS v1.0</span>
          </CardTitle>
          <CardDescription className="text-muted-foreground">
            [theProjectCompany] Artist Management System v1.0
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="admin@theprojectcompany.kr"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            </div>
            <CardFooter className="flex flex-col mt-6 p-0">
              <Button type="submit" className="w-full btn-orange rounded-md" disabled={loading}>
                {loading ? 'Logging in...' : 'Login'}
              </Button>
              <a href="/signup" className="text-sm text-primary hover:underline mt-4">
                Don't have an account? Sign up
              </a>
            </CardFooter>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default Login;