"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Rocket, AlertCircle, GraduationCap, User as UserIcon } from "lucide-react";
import { cn } from "@/lib/utils";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();

  const [role, setRole] = useState<"candidate" | "expert">("candidate");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const result = await login(email, password);
    setLoading(false);

    if (result.success) {
      if (result.user?.role === "expert" || role === "expert") {
        router.push("/expert");
      } else {
        router.push("/resume");
      }
    } else {
      setError(result.error || "Failed to log in. Please check your credentials.");
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-muted/30 p-4 py-8">
      <div className="w-full max-w-md space-y-6">
        <div className="flex flex-col items-center gap-2 mb-6">
          <div className="h-12 w-12 bg-primary/10 rounded-2xl border border-primary/20 flex items-center justify-center">
            <Rocket className="h-6 w-6 text-primary" />
          </div>
          <h1 className="text-2xl font-bold">Welcome back to PrepPilot</h1>
          <p className="text-sm text-muted-foreground">Sign in to access your dashboard</p>
        </div>

        <Card className="border-border/80 shadow-lg">
          <form onSubmit={handleSubmit}>
            <CardHeader>
              <CardTitle>Log In</CardTitle>
              <CardDescription>Enter your email and password below</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div
                  onClick={() => setRole("candidate")}
                  className={cn(
                    "flex flex-col items-center justify-center gap-2 p-3 border rounded-lg cursor-pointer transition-colors",
                    role === "candidate"
                      ? "border-primary bg-primary/10 text-primary"
                      : "border-border hover:bg-muted text-muted-foreground"
                  )}
                >
                  <UserIcon className="w-5 h-5" />
                  <span className="text-sm font-medium">Student</span>
                </div>
                <div
                  onClick={() => setRole("expert")}
                  className={cn(
                    "flex flex-col items-center justify-center gap-2 p-3 border rounded-lg cursor-pointer transition-colors",
                    role === "expert"
                      ? "border-primary bg-primary/10 text-primary"
                      : "border-border hover:bg-muted text-muted-foreground"
                  )}
                >
                  <GraduationCap className="w-5 h-5" />
                  <span className="text-sm font-medium">Mentor</span>
                </div>
              </div>

              {error && (
                <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive text-sm flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <span>{error}</span>
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="name@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="password">Password</Label>
                  <Link href="#" className="text-xs text-primary hover:underline">Forgot password?</Link>
                </div>
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <Button type="submit" className="w-full mt-2" disabled={loading}>
                {loading ? "Authenticating..." : "Log In"}
              </Button>
            </CardContent>
          </form>

          <CardFooter className="flex flex-col gap-4 border-t pt-4">
            <div className="text-sm text-center text-muted-foreground w-full">
              Don't have an account?{" "}
              <Link href="/signup" className="text-primary font-medium hover:underline">
                Sign up
              </Link>
            </div>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
