"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Rocket } from "lucide-react";
import { login } from "@/lib/booking-api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const session = await login(email, password);
      router.push(session.user.role === "expert" ? "/availability" : "/bookings");
      router.refresh();
    } catch (authError) {
      setError(authError instanceof Error ? authError.message : "Could not log in.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-muted/30 p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="flex flex-col items-center gap-2 mb-8">
          <div className="h-12 w-12 bg-primary/10 rounded-full flex items-center justify-center">
            <Rocket className="h-6 w-6 text-primary" />
          </div>
          <h1 className="text-2xl font-bold">Welcome back to PrepPilot</h1>
          <p className="text-sm text-muted-foreground">Enter your credentials to access your account</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Log In</CardTitle>
            <CardDescription>Enter your email and password below</CardDescription>
          </CardHeader>
          <form onSubmit={submit}>
          <CardContent className="space-y-4">
            {error && <div role="alert" className="rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-800">{error}</div>}
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="m@example.com" value={email} onChange={event => setEmail(event.target.value)} autoComplete="email" required />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password">Password</Label>
                <Link href="#" className="text-sm text-primary hover:underline">Forgot password?</Link>
              </div>
              <Input id="password" type="password" value={password} onChange={event => setPassword(event.target.value)} autoComplete="current-password" required />
            </div>
            <Button className="w-full mt-4" disabled={loading}>{loading ? "Logging in…" : "Log In"}</Button>
          </CardContent>
          </form>
          <CardFooter className="flex flex-col gap-4">
            <div className="text-sm text-center text-muted-foreground w-full">
              Don&apos;t have an account?{" "}
              <Link href="/signup" className="text-primary font-medium hover:underline">
                Sign up
              </Link>
            </div>
            <div className="relative w-full">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">Or</span>
              </div>
            </div>
            <Link href="/resume" className="w-full">
              <Button variant="outline" className="w-full">Continue as Guest</Button>
            </Link>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
