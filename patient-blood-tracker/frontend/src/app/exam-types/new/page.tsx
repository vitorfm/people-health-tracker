"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function NewExamTypePage() {
  const router = useRouter();
  const [form, setForm] = useState({
    name: "",
    description: "",
    male_min: "",
    male_max: "",
    female_min: "",
    female_max: "",
    child_min: "",
    child_max: ""
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
      const reference_values: any = {};
      if (form.male_min && form.male_max) reference_values.male = { min: parseFloat(form.male_min), max: parseFloat(form.male_max) };
      if (form.female_min && form.female_max) reference_values.female = { min: parseFloat(form.female_min), max: parseFloat(form.female_max) };
      if (form.child_min && form.child_max) reference_values.child = { min: parseFloat(form.child_min), max: parseFloat(form.child_max) };
      const res = await fetch("http://localhost:8000/api/v1/exam-types/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: form.name,
          description: form.description,
          reference_values
        })
      });
      if (!res.ok) throw new Error("Error creating exam type");
      router.push("/exam-types");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">New Exam Type</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="name" placeholder="Name" className="w-full border px-2 py-1" value={form.name} onChange={handleChange} required />
        <textarea name="description" placeholder="Description" className="w-full border px-2 py-1" value={form.description} onChange={handleChange} required />
        <div className="grid grid-cols-3 gap-2">
          <div>
            <label className="block font-bold">Male</label>
            <input name="male_min" type="number" step="any" placeholder="Min" className="w-full border px-2 py-1" value={form.male_min} onChange={handleChange} />
            <input name="male_max" type="number" step="any" placeholder="Max" className="w-full border px-2 py-1" value={form.male_max} onChange={handleChange} />
          </div>
          <div>
            <label className="block font-bold">Female</label>
            <input name="female_min" type="number" step="any" placeholder="Min" className="w-full border px-2 py-1" value={form.female_min} onChange={handleChange} />
            <input name="female_max" type="number" step="any" placeholder="Max" className="w-full border px-2 py-1" value={form.female_max} onChange={handleChange} />
          </div>
          <div>
            <label className="block font-bold">Child</label>
            <input name="child_min" type="number" step="any" placeholder="Min" className="w-full border px-2 py-1" value={form.child_min} onChange={handleChange} />
            <input name="child_max" type="number" step="any" placeholder="Max" className="w-full border px-2 py-1" value={form.child_max} onChange={handleChange} />
          </div>
        </div>
        {error && <p className="text-red-600">{error}</p>}
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>{loading ? "Saving..." : "Save"}</button>
      </form>
    </div>
  );
} 