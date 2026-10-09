"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Rocket, User, GraduationCap } from "lucide-react";
import { cn } from "cn";
import { login, signup } from "@/lib/booking-api";

export default function SignupPage() {
  const router = useRouter();
  const [role, setRole] = useState<"candidate" | "expert">("candidate");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      await signup(name, email, password, role);
      await login(email, password);
      router.push(role === "expert" ? "/availability" : "/bookings");
    } catch (authError) {
      setError(authError instanceof Error ? authError.message : "Could not create your account.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-muted/30 p-4 py-12">
      <div className="w-full max-w-md space-y-6">
        <div className="flex flex-col items-center gap-2 mb-8">
          <div className="h-12 w-12 bg-primary/10 rounded-full flex items-center justify-center">
            <Rocket className="h-6 w-6 text-primary" />
          </div>
          <h1 className="text-2xl font-bold">Join PrepPilot</h1>
          <p className="text-sm text-muted-foreground">Create an account to start your journey</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Create an account</CardTitle>
            <CardDescription>Enter your details below to create your account</CardDescription>
          </CardHeader>
          <form onSubmit={submit}>
          <CardContent className="space-y-4">
            {error && <div role="alert" className="rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-800">{error}</div>}
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div 
                className={cn(
                  "border rounded-xl p-4 flex flex-col items-center gap-2 cursor-pointer transition-all",
                  role === "candidate" ? "border-primary bg-primary/5 ring-1 ring-primary" : "hover:bg-muted"
                )}
                onClick={() => setRole("candidate")}
              >
                <User className={cn("h-6 w-6", role === "candidate" ? "text-primary" : "text-muted-foreground")} />
                <span className="text-sm font-medium">I&apos;m a Candidate</span>
              </div>
              <div 
                className={cn(
                  "border rounded-xl p-4 flex flex-col items-center gap-2 cursor-pointer transition-all",
                  role === "expert" ? "border-primary bg-primary/5 ring-1 ring-primary" : "hover:bg-muted"
                )}
                onClick={() => setRole("expert")}
              >
                <GraduationCap className={cn("h-6 w-6", role === "expert" ? "text-primary" : "text-muted-foreground")} />
                <span className="text-sm font-medium">I&apos;m an Expert</span>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="name">Full Name</Label>
              <Input id="name" placeholder="John Doe" value={name} onChange={event => setName(event.target.value)} autoComplete="name" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="m@example.com" value={email} onChange={event => setEmail(event.target.value)} autoComplete="email" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" minLength={8} value={password} onChange={event => setPassword(event.target.value)} autoComplete="new-password" required />
            </div>
            <Button className="w-full mt-4" disabled={loading}>{loading ? "Creating account…" : "Create Account"}</Button>
          </CardContent>
          </form>
          <CardFooter>
            <div className="text-sm text-center text-muted-foreground w-full">
              Already have an account?{" "}
              <Link href="/login" className="text-primary font-medium hover:underline">
                Log in
              </Link>
            </div>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
