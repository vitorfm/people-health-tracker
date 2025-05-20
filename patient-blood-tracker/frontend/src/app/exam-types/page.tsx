"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

interface ReferenceRange {
  min: number;
  max: number;
}

interface ExamType {
  id: string;
  name: string;
  description: string;
  reference_values: {
    male?: ReferenceRange;
    female?: ReferenceRange;
    child?: ReferenceRange;
  };
}

export default function ExamTypesPage() {
  const [examTypes, setExamTypes] = useState<ExamType[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/exam-types/")
      .then((res) => res.json())
      .then((data) => {
        setExamTypes(Array.isArray(data) ? data : []);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Exam Types</h1>
        <Link href="/exam-types/new" className="bg-blue-600 text-white px-4 py-2 rounded">New Exam Type</Link>
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : examTypes.length === 0 ? (
        <p>No exam types found.</p>
      ) : (
        <table className="min-w-full border">
          <thead>
            <tr>
              <th className="border px-2 py-1">Name</th>
              <th className="border px-2 py-1">Description</th>
              <th className="border px-2 py-1">Reference Values</th>
            </tr>
          </thead>
          <tbody>
            {examTypes.map((et, idx) => (
              <tr key={et.id || idx}>
                <td className="border px-2 py-1">{et.name}</td>
                <td className="border px-2 py-1">{et.description}</td>
                <td className="border px-2 py-1">
                  {Object.entries(et.reference_values).map(([group, range]) => (
                    <div key={group}>
                      <b>{group}:</b> {range.min} - {range.max}
                    </div>
                  ))}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
} 