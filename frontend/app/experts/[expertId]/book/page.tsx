"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { CalendarCheck, ChevronLeft, Clock3, Rocket } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { AvailabilitySlot, createBooking, listExpertSlots } from "@/lib/booking-api";
import { formatDateTime } from "@/lib/date";

export default function BookExpertPage() {
  const { expertId } = useParams<{ expertId: string }>();
  const router = useRouter();
  const [slots, setSlots] = useState<AvailabilitySlot[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(true);
  const [booking, setBooking] = useState(false);
  const [error, setError] = useState("");

  const [range] = useState(() => ({ start: new Date(), end: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000) }));
  const load = useCallback(async () => {
    try {
      setSlots(await listExpertSlots(expertId, range.start, range.end));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load available times.");
    } finally {
      setLoading(false);
    }
  }, [expertId, range]);

  useEffect(() => { queueMicrotask(() => void load()); }, [load]);

  async function confirm() {
    if (!selected) return;
    setBooking(true);
    setError("");
    try {
      await createBooking(selected, notes.trim());
      router.push("/bookings?booked=1");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not complete the booking.");
      await load();
    } finally {
      setBooking(false);
    }
  }

  return (
    <div className="min-h-screen bg-muted/20">
      <header className="border-b bg-background"><div className="container mx-auto flex h-16 items-center justify-between px-4"><Link href="/" className="flex items-center gap-2 font-bold"><Rocket className="h-5 w-5 text-primary" />PrepPilot</Link><Link href="/bookings"><Button variant="outline">My bookings</Button></Link></div></header>
      <main className="container mx-auto max-w-4xl px-4 py-10">
        <button onClick={() => router.back()} className="mb-6 flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"><ChevronLeft className="h-4 w-4" />Back to expert</button>
        <h1 className="text-3xl font-bold">Choose an interview time</h1>
        <p className="mt-2 text-muted-foreground">Times are shown in your local timezone. Your slot is only reserved after confirmation.</p>
        {error && <div role="alert" className="mt-6 rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">{error}</div>}
        <div className="mt-8 grid gap-6 md:grid-cols-[1fr_320px]">
          <Card>
            <CardHeader><CardTitle>Available slots</CardTitle><CardDescription>Next 60 days</CardDescription></CardHeader>
            <CardContent className="grid gap-3 sm:grid-cols-2">
              {loading && <p className="col-span-full py-10 text-center text-muted-foreground">Loading available times…</p>}
              {!loading && slots.length === 0 && <div className="col-span-full rounded-lg border border-dashed py-10 text-center"><CalendarCheck className="mx-auto mb-3 h-8 w-8 text-muted-foreground" /><p className="font-medium">No available times</p><p className="mt-1 text-sm text-muted-foreground">Check again later for newly published slots.</p></div>}
              {slots.map(slot => <button key={slot.id} type="button" onClick={() => setSelected(slot.id)} className={`rounded-xl border p-4 text-left transition ${selected === slot.id ? "border-primary bg-primary/5 ring-2 ring-primary/20" : "hover:border-primary/50"}`}>
                <p className="font-semibold">{formatDateTime(slot.start_time)}</p><p className="mt-2 flex items-center gap-1 text-sm text-muted-foreground"><Clock3 className="h-4 w-4" />Ends {formatDateTime(slot.end_time)}</p>
              </button>)}
            </CardContent>
          </Card>
          <Card className="h-fit">
            <CardHeader><CardTitle>Booking details</CardTitle><CardDescription>{selected ? formatDateTime(slots.find(slot => slot.id === selected)?.start_time || "") : "Select a time to continue"}</CardDescription></CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2"><Label htmlFor="notes">Focus areas or notes (optional)</Label><Textarea id="notes" maxLength={500} value={notes} onChange={event => setNotes(event.target.value)} placeholder="e.g. System design for a backend role" /><p className="text-right text-xs text-muted-foreground">{notes.length}/500</p></div>
              <Button className="w-full" disabled={!selected || booking} onClick={confirm}>{booking ? "Reserving…" : "Confirm booking"}</Button>
              <p className="text-xs leading-relaxed text-muted-foreground">Confirmation is atomic. If another candidate reserves this time first, you’ll be asked to choose another slot.</p>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
