"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function NewDoctorPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    name: "",
    email: "",
    date_of_birth: "",
    gender: "",
    phone: "",
    address: "",
    notes: "",
    specialty: ""
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:8000/api/v1/doctors/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });
      if (!res.ok) throw new Error("Error creating doctor");
      router.push("/doctors");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">New Doctor</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="name" placeholder="Name" className="w-full border px-2 py-1" value={form.name} onChange={handleChange} required />
        <input name="email" placeholder="Email" className="w-full border px-2 py-1" value={form.email} onChange={handleChange} required />
        <input name="date_of_birth" type="date" placeholder="Date of Birth" className="w-full border px-2 py-1" value={form.date_of_birth} onChange={handleChange} required />
        <input name="gender" placeholder="Gender" className="w-full border px-2 py-1" value={form.gender} onChange={handleChange} required />
        <input name="phone" placeholder="Phone" className="w-full border px-2 py-1" value={form.phone} onChange={handleChange} required />
        <input name="address" placeholder="Address" className="w-full border px-2 py-1" value={form.address} onChange={handleChange} />
        <textarea name="notes" placeholder="Notes" className="w-full border px-2 py-1" value={form.notes} onChange={handleChange} />
        <input name="specialty" placeholder="Specialty" className="w-full border px-2 py-1" value={form.specialty} onChange={handleChange} required />
        {error && <p className="text-red-600">{error}</p>}
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>{loading ? "Saving..." : "Save"}</button>
      </form>
    </div>
  );
} 