export interface AvailabilitySlot {
  id: string;
  expert_id: string;
  start_time: string;
  end_time: string;
  is_booked: boolean;
}

export interface Booking {
  id: string;
  candidate_id: string;
  expert_id: string;
  slot_id: string;
  status: "scheduled" | "completed" | "cancelled" | "no_show";
  session_type: string;
  notes: string | null;
  start_time: string;
  end_time: string;
  created_at: string;
  cancelled_at: string | null;
  cancellation_reason: string | null;
}

interface Envelope<T> {
  data: T | null;
  error: { message: string } | null;
}

export interface AuthUser {
  id: string;
  email: string;
  full_name: string | null;
  role: "candidate" | "expert";
}

interface AuthSession {
  token: string;
  user: AuthUser;
}

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function request<T>(path: string, init: RequestInit = {}, authenticated = true): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");

  if (authenticated) {
    const token = typeof window === "undefined" ? null : localStorage.getItem("preppilot_access_token");
    if (!token) throw new Error("Please sign in to continue.");
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${BASE_URL}${path}`, { ...init, headers });
  let envelope: Envelope<T>;
  try {
    envelope = await response.json();
  } catch {
    throw new Error("The booking service returned an invalid response.");
  }
  if (!response.ok || envelope.error || envelope.data === null) {
    throw new Error(envelope.error?.message || `Request failed (${response.status})`);
  }
  return envelope.data;
}

export function listExpertSlots(expertId: string, start: Date, end: Date, includeBooked = false) {
  const query = new URLSearchParams({
    start: start.toISOString(),
    end: end.toISOString(),
    include_booked: String(includeBooked),
  });
  return request<AvailabilitySlot[]>(`/api/availability/experts/${encodeURIComponent(expertId)}?${query}`, {}, false);
}

export function createAvailability(slots: Array<{ start_time: string; end_time: string }>) {
  return request<AvailabilitySlot[]>("/api/availability", {
    method: "POST",
    body: JSON.stringify({ slots }),
  });
}

export function deleteAvailability(slotId: string) {
  return request<{ deleted: boolean }>(`/api/availability/${encodeURIComponent(slotId)}`, { method: "DELETE" });
}

export function createBooking(slotId: string, notes?: string) {
  return request<Booking>("/api/bookings", {
    method: "POST",
    body: JSON.stringify({ slot_id: slotId, notes: notes || null }),
  });
}

export function listMyBookings(view: "candidate" | "expert") {
  return request<Booking[]>(`/api/bookings/me?view=${view}`);
}

export function cancelBooking(bookingId: string, reason?: string) {
  return request<Booking>(`/api/bookings/${encodeURIComponent(bookingId)}/cancel`, {
    method: "POST",
    body: JSON.stringify({ reason: reason || null }),
  });
}

export function bootstrapUser() {
  return request<{ id: string; email: string; role: string; expert_approval_required: boolean }>(
    "/api/auth/bootstrap",
    { method: "POST", body: "{}" },
  );
}

export async function login(email: string, password: string) {
  const session = await request<AuthSession>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  }, false);
  localStorage.setItem("preppilot_access_token", session.token);
  localStorage.setItem("preppilot_user", JSON.stringify(session.user));
  return session;
}

export async function signup(fullName: string, email: string, password: string, role: "candidate" | "expert") {
  return request<AuthUser>("/api/auth/signup", {
    method: "POST",
    body: JSON.stringify({ full_name: fullName, email, password, role }),
  }, false);
}

export function getCurrentUser() {
  return request<AuthUser>("/api/auth/me");
}

export function logout() {
  localStorage.removeItem("preppilot_access_token");
  localStorage.removeItem("preppilot_user");
}
