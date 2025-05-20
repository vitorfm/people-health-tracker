"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

interface Paciente {
  id: string;
  name: string;
  email: string;
  date_of_birth: string;
  gender: string;
  phone: string;
}

export default function PacientesPage() {
  const [pacientes, setPacientes] = useState<Paciente[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/patients/")
      .then((res) => res.json())
      .then((data) => {
        setPacientes(data);
        setLoading(false);
      });
  }, []);

  const pacientesArray = Array.isArray(pacientes) ? pacientes : [];

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Pacientes</h1>
        <Link href="/pacientes/novo" className="bg-blue-600 text-white px-4 py-2 rounded">Novo Paciente</Link>
      </div>
      {loading ? (
        <p>Carregando...</p>
      ) : (
        <table className="min-w-full border">
          <thead>
            <tr>
              <th className="border px-2 py-1">Nome</th>
              <th className="border px-2 py-1">Email</th>
              <th className="border px-2 py-1">Nascimento</th>
              <th className="border px-2 py-1">Gênero</th>
              <th className="border px-2 py-1">Telefone</th>
            </tr>
          </thead>
          <tbody>
            {pacientesArray.map((p, idx) => (
              <tr key={p.id || idx}>
                <td className="border px-2 py-1">{p.name}</td>
                <td className="border px-2 py-1">{p.email}</td>
                <td className="border px-2 py-1">{new Date(p.date_of_birth).toLocaleDateString()}</td>
                <td className="border px-2 py-1">{p.gender}</td>
                <td className="border px-2 py-1">{p.phone}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
} 