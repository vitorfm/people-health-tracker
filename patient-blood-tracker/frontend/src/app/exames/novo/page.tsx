"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

interface Patient {
  id: string;
  name: string;
}
interface ExamType {
  id: string;
  name: string;
}
interface Doctor {
  id: string;
  name: string;
}
interface ExamResultForm {
  exam_type_id: string;
  value: string;
}

export default function NewExamPage() {
  const router = useRouter();
  const [patients, setPatients] = useState<Patient[]>([]);
  const [examTypes, setExamTypes] = useState<ExamType[]>([]);
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [form, setForm] = useState({
    patient_id: "",
    test_date: "",
    exam_types: [] as string[],
    results: [] as ExamResultForm[],
    notes: "",
    doctor_id: "",
    lab_name: ""
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/patients/")
      .then((res) => res.json())
      .then((data) => setPatients(Array.isArray(data) ? data : []));
    fetch("http://localhost:8000/api/v1/exam-types/")
      .then((res) => res.json())
      .then((data) => setExamTypes(Array.isArray(data) ? data : []));
    fetch("http://localhost:8000/api/v1/doctors/")
      .then((res) => res.json())
      .then((data) => setDoctors(Array.isArray(data) ? data : []));
  }, []);

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) {
    const { name, value, type, options } = e.target as HTMLSelectElement;
    if (type === "select-multiple") {
      const selected = Array.from(options).filter(o => o.selected).map(o => o.value);
      setForm({ ...form, [name]: selected });
    } else {
      setForm({ ...form, [name]: value });
    }
  }

  function handleResultChange(idx: number, field: string, value: string) {
    const newResults = [...form.results];
    newResults[idx] = { ...newResults[idx], [field]: value };
    setForm({ ...form, results: newResults });
  }

  function addResult() {
    setForm({ ...form, results: [...form.results, { exam_type_id: "", value: "" }] });
  }

  function removeResult(idx: number) {
    const newResults = [...form.results];
    newResults.splice(idx, 1);
    setForm({ ...form, results: newResults });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const results = form.results.map(r => ({ exam_type_id: r.exam_type_id, value: parseFloat(r.value) }));
      const res = await fetch("http://localhost:8000/api/v1/blood-tests/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          results,
        })
      });
      if (!res.ok) throw new Error("Error creating exam");
      router.push("/exames");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">New Exam</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <select name="patient_id" className="w-full border px-2 py-1" value={form.patient_id} onChange={handleChange} required>
          <option value="">Select patient</option>
          {patients.map((p, idx) => (
            <option key={p.id || idx} value={p.id}>{p.name}</option>
          ))}
        </select>
        <input name="test_date" type="date" className="w-full border px-2 py-1" value={form.test_date} onChange={handleChange} required />
        <select name="exam_types" multiple className="w-full border px-2 py-1" value={form.exam_types} onChange={handleChange} required>
          {examTypes.map((et, idx) => (
            <option key={et.id || idx} value={et.id}>{et.name}</option>
          ))}
        </select>
        <div>
          <label className="block font-bold mb-2">Exam Results</label>
          {form.results.map((r, idx) => (
            <div key={idx} className="flex gap-2 mb-2 items-center">
              <select value={r.exam_type_id} onChange={e => handleResultChange(idx, "exam_type_id", e.target.value)} className="border px-2 py-1">
                <option value="">Select type</option>
                {examTypes.map((et, i) => (
                  <option key={et.id || i} value={et.id}>{et.name}</option>
                ))}
              </select>
              <input type="number" step="any" placeholder="Value" value={r.value} onChange={e => handleResultChange(idx, "value", e.target.value)} className="border px-2 py-1" />
              <button type="button" onClick={() => removeResult(idx)} className="text-red-600">Remove</button>
            </div>
          ))}
          <button type="button" onClick={addResult} className="bg-gray-200 px-2 py-1 rounded">Add Result</button>
        </div>
        <textarea name="notes" placeholder="Notes" className="w-full border px-2 py-1" value={form.notes} onChange={handleChange} />
        <select name="doctor_id" className="w-full border px-2 py-1" value={form.doctor_id} onChange={handleChange} required>
          <option value="">Select doctor</option>
          {doctors.map((d, idx) => (
            <option key={d.id || idx} value={d.id}>{d.name}</option>
          ))}
        </select>
        <input name="lab_name" placeholder="Lab name" className="w-full border px-2 py-1" value={form.lab_name} onChange={handleChange} required />
        {error && <p className="text-red-600">{error}</p>}
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>{loading ? "Saving..." : "Save"}</button>
      </form>
    </div>
  );
} 