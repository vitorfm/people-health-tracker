"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

interface Doctor {
  id: string;
  name: string;
  email: string;
  specialty: string;
}

export default function DoctorsPage() {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/doctors/")
      .then((res) => res.json())
      .then((data) => {
        setDoctors(Array.isArray(data) ? data : []);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Doctors</h1>
        <Link href="/doctors/new" className="bg-blue-600 text-white px-4 py-2 rounded">New Doctor</Link>
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : doctors.length === 0 ? (
        <p>No doctors found.</p>
      ) : (
        <table className="min-w-full border">
          <thead>
            <tr>
              <th className="border px-2 py-1">Name</th>
              <th className="border px-2 py-1">Email</th>
              <th className="border px-2 py-1">Specialty</th>
            </tr>
          </thead>
          <tbody>
            {doctors.map((d, idx) => (
              <tr key={d.id || idx}>
                <td className="border px-2 py-1">{d.name}</td>
                <td className="border px-2 py-1">{d.email}</td>
                <td className="border px-2 py-1">{d.specialty}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
} 