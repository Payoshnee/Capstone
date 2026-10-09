"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { CalendarDays, Clock3, Plus, Rocket, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { AvailabilitySlot, createAvailability, deleteAvailability, getCurrentUser, listExpertSlots } from "@/lib/booking-api";
import { formatDateTime, localInputValue } from "@/lib/date";

export default function AvailabilityPage() {
  const [initialTimes] = useState(() => {
    const initialStart = new Date(Date.now() + 60 * 60 * 1000);
    initialStart.setMinutes(0, 0, 0);
    return {
      start: localInputValue(initialStart),
      end: localInputValue(new Date(initialStart.getTime() + 60 * 60 * 1000)),
    };
  });
  const [start, setStart] = useState(initialTimes.start);
  const [end, setEnd] = useState(initialTimes.end);
  const [repeatWeeks, setRepeatWeeks] = useState(1);
  const [slots, setSlots] = useState<AvailabilitySlot[]>([]);
  const [expertId, setExpertId] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async (id: string) => {
    setLoading(true);
    try {
      const from = new Date();
      const to = new Date(Date.now() + 90 * 24 * 60 * 60 * 1000);
      setSlots(await listExpertSlots(id, from, to, true));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load availability.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    getCurrentUser().then(user => {
      const id = user.id;
      setExpertId(id);
      if (id) load(id);
    }).catch(err => {
      setError(err instanceof Error ? err.message : "Please sign in with your approved expert account.");
      setLoading(false);
    });
  }, [load]);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setSuccess("");
    const startDate = new Date(start);
    const endDate = new Date(end);
    if (endDate <= startDate) return setError("End time must be after start time.");
    try {
      const slots = Array.from({ length: repeatWeeks }, (_, index) => ({
        start_time: new Date(startDate.getTime() + index * 7 * 24 * 60 * 60 * 1000).toISOString(),
        end_time: new Date(endDate.getTime() + index * 7 * 24 * 60 * 60 * 1000).toISOString(),
      }));
      await createAvailability(slots);
      setSuccess(`${slots.length} availability ${slots.length === 1 ? "slot" : "slots"} published.`);
      if (expertId) await load(expertId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not add availability.");
    }
  }

  async function remove(slot: AvailabilitySlot) {
    setError("");
    try {
      await deleteAvailability(slot.id);
      setSlots(current => current.filter(item => item.id !== slot.id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not remove availability.");
    }
  }

  return (
    <div className="min-h-screen bg-muted/20">
      <header className="border-b bg-background">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <Link href="/" className="flex items-center gap-2 font-bold"><Rocket className="h-5 w-5 text-primary" />PrepPilot</Link>
          <Link href="/bookings"><Button variant="outline">View bookings</Button></Link>
        </div>
      </header>
      <main className="container mx-auto max-w-5xl px-4 py-10">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Manage availability</h1>
          <p className="mt-2 text-muted-foreground">Publish interview times in your timezone. PrepPilot stores them safely in UTC.</p>
        </div>
        {error && <div role="alert" className="mb-5 rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">{error}</div>}
        {success && <div role="status" className="mb-5 rounded-lg border border-green-300 bg-green-50 p-4 text-sm text-green-800">{success}</div>}
        <div className="grid gap-6 lg:grid-cols-[360px_1fr]">
          <Card>
            <CardHeader><CardTitle className="flex items-center gap-2"><Plus className="h-5 w-5" />Add a time</CardTitle><CardDescription>Slots can be 15 minutes to 4 hours long.</CardDescription></CardHeader>
            <CardContent>
              <form onSubmit={submit} className="space-y-5">
                <div className="space-y-2"><Label htmlFor="start">Starts</Label><Input id="start" type="datetime-local" value={start} onChange={event => setStart(event.target.value)} required /></div>
                <div className="space-y-2"><Label htmlFor="end">Ends</Label><Input id="end" type="datetime-local" value={end} onChange={event => setEnd(event.target.value)} required /></div>
                <div className="space-y-2"><Label htmlFor="repeat">Repeat weekly</Label><select id="repeat" value={repeatWeeks} onChange={event => setRepeatWeeks(Number(event.target.value))} className="h-9 w-full rounded-md border border-input bg-transparent px-3 text-sm shadow-xs outline-none focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50">{Array.from({ length: 8 }, (_, index) => <option key={index + 1} value={index + 1}>{index + 1} {index === 0 ? "week" : "weeks"}</option>)}</select></div>
                <Button className="w-full" disabled={!expertId}>Publish availability</Button>
              </form>
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="flex items-center gap-2"><CalendarDays className="h-5 w-5" />Upcoming times</CardTitle><CardDescription>Booked times remain visible and cannot be deleted.</CardDescription></CardHeader>
            <CardContent className="space-y-3">
              {loading && <p className="py-8 text-center text-muted-foreground">Loading availability…</p>}
              {!loading && slots.length === 0 && <p className="rounded-lg border border-dashed py-10 text-center text-muted-foreground">No upcoming availability yet.</p>}
              {slots.map(slot => <div key={slot.id} className="flex items-center justify-between gap-4 rounded-xl border p-4">
                <div><p className="font-medium">{formatDateTime(slot.start_time)}</p><p className="mt-1 flex items-center gap-1 text-sm text-muted-foreground"><Clock3 className="h-4 w-4" />Until {formatDateTime(slot.end_time)}</p></div>
                {slot.is_booked ? <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-800">Booked</span> : <Button variant="ghost" size="icon" aria-label="Delete slot" onClick={() => remove(slot)}><Trash2 className="h-4 w-4 text-red-600" /></Button>}
              </div>)}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
