"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function NovoPacientePage() {
  const router = useRouter();
  const [form, setForm] = useState({
    name: "",
    email: "",
    date_of_birth: "",
    gender: "",
    phone: "",
    address: "",
    diseases: "",
    notes: ""
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
      const res = await fetch("http://localhost:8000/api/v1/patients/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          diseases: form.diseases.split(",").map((d) => d.trim()).filter(Boolean)
        })
      });
      if (!res.ok) throw new Error("Erro ao cadastrar paciente");
      router.push("/pacientes");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Novo Paciente</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="name" placeholder="Nome" className="w-full border px-2 py-1" value={form.name} onChange={handleChange} required />
        <input name="email" placeholder="Email" className="w-full border px-2 py-1" value={form.email} onChange={handleChange} required />
        <input name="date_of_birth" type="date" placeholder="Nascimento" className="w-full border px-2 py-1" value={form.date_of_birth} onChange={handleChange} required />
        <input name="gender" placeholder="Gênero" className="w-full border px-2 py-1" value={form.gender} onChange={handleChange} required />
        <input name="phone" placeholder="Telefone" className="w-full border px-2 py-1" value={form.phone} onChange={handleChange} required />
        <input name="address" placeholder="Endereço" className="w-full border px-2 py-1" value={form.address} onChange={handleChange} />
        <input name="diseases" placeholder="Doenças (separadas por vírgula)" className="w-full border px-2 py-1" value={form.diseases} onChange={handleChange} />
        <textarea name="notes" placeholder="Notas" className="w-full border px-2 py-1" value={form.notes} onChange={handleChange} />
        {error && <p className="text-red-600">{error}</p>}
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>{loading ? "Salvando..." : "Salvar"}</button>
      </form>
    </div>
  );
} 