"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { CalendarDays, Clock3, Rocket, XCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Booking, cancelBooking, listMyBookings } from "@/lib/booking-api";
import { formatDateTime } from "@/lib/date";

function BookingList({ items, onCancel }: { items: Booking[]; onCancel: (booking: Booking) => void }) {
  if (!items.length) return <div className="rounded-xl border border-dashed py-12 text-center"><CalendarDays className="mx-auto mb-3 h-9 w-9 text-muted-foreground" /><p className="font-medium">No bookings yet</p><p className="mt-1 text-sm text-muted-foreground">Your scheduled interviews will appear here.</p></div>;
  return <div className="space-y-3">{items.map(item => <div key={item.id} className="flex flex-col justify-between gap-4 rounded-xl border p-5 sm:flex-row sm:items-center">
    <div><div className="flex items-center gap-2"><p className="font-semibold">{formatDateTime(item.start_time)}</p><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${item.status === "scheduled" ? "bg-green-100 text-green-800" : item.status === "cancelled" ? "bg-gray-100 text-gray-700" : "bg-blue-100 text-blue-800"}`}>{item.status}</span></div><p className="mt-2 flex items-center gap-1 text-sm text-muted-foreground"><Clock3 className="h-4 w-4" />Ends {formatDateTime(item.end_time)}</p>{item.notes && <p className="mt-2 text-sm">Focus: {item.notes}</p>}</div>
    {item.status === "scheduled" && new Date(item.start_time) > new Date() && <Button variant="outline" onClick={() => onCancel(item)}><XCircle className="mr-2 h-4 w-4" />Cancel</Button>}
  </div>)}</div>;
}

export default function BookingsPage() {
  const [view, setView] = useState<"candidate" | "expert">("candidate");
  const [items, setItems] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const load = useCallback(async (selectedView: "candidate" | "expert") => {
    try { setItems(await listMyBookings(selectedView)); }
    catch (err) { setError(err instanceof Error ? err.message : "Could not load bookings."); }
    finally { setLoading(false); }
  }, []);
  useEffect(() => {
    const booked = new URLSearchParams(window.location.search).get("booked");
    if (booked) queueMicrotask(() => setNotice("Your interview is confirmed."));
  }, []);
  useEffect(() => { queueMicrotask(() => void load(view)); }, [load, view]);

  async function cancel(item: Booking) {
    if (!window.confirm("Cancel this interview? The time will become available to other candidates.")) return;
    try { await cancelBooking(item.id); setNotice("Booking cancelled successfully."); await load(view); }
    catch (err) { setError(err instanceof Error ? err.message : "Could not cancel booking."); }
  }

  return <div className="min-h-screen bg-muted/20">
    <header className="border-b bg-background"><div className="container mx-auto flex h-16 items-center justify-between px-4"><Link href="/" className="flex items-center gap-2 font-bold"><Rocket className="h-5 w-5 text-primary" />PrepPilot</Link><Link href="/availability"><Button variant="outline">Manage availability</Button></Link></div></header>
    <main className="container mx-auto max-w-4xl px-4 py-10"><h1 className="text-3xl font-bold">Bookings</h1><p className="mt-2 text-muted-foreground">Manage upcoming and previous mock interviews.</p>
      {error && <div role="alert" className="mt-6 rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">{error}</div>}{notice && <div role="status" className="mt-6 rounded-lg border border-green-300 bg-green-50 p-4 text-sm text-green-800">{notice}</div>}
      <Card className="mt-8"><CardHeader><CardTitle>Interview schedule</CardTitle><CardDescription>Switch between interviews you booked and interviews candidates booked with you.</CardDescription></CardHeader><CardContent>
        <Tabs value={view} onValueChange={value => { setLoading(true); setView(value as "candidate" | "expert"); }}><TabsList className="mb-6"><TabsTrigger value="candidate">As candidate</TabsTrigger><TabsTrigger value="expert">As expert</TabsTrigger></TabsList><TabsContent value="candidate">{loading ? <p className="py-10 text-center text-muted-foreground">Loading bookings…</p> : <BookingList items={items} onCancel={cancel} />}</TabsContent><TabsContent value="expert">{loading ? <p className="py-10 text-center text-muted-foreground">Loading bookings…</p> : <BookingList items={items} onCancel={cancel} />}</TabsContent></Tabs>
      </CardContent></Card>
    </main>
  </div>;
}
