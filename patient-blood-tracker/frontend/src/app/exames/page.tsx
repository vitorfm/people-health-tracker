"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

interface Exam {
  id: string;
  patient_id: string;
  test_date: string;
  exam_types: string[];
  results: Record<string, number>;
  notes?: string;
  doctor_id?: string;
  lab_name: string;
}

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

export default function ExamsPage() {
  const [exams, setExams] = useState<Exam[]>([]);
  const [patients, setPatients] = useState<Patient[]>([]);
  const [examTypes, setExamTypes] = useState<ExamType[]>([]);
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch("http://localhost:8000/api/v1/blood-tests/").then((res) => res.json()),
      fetch("http://localhost:8000/api/v1/patients/").then((res) => res.json()),
      fetch("http://localhost:8000/api/v1/exam-types/").then((res) => res.json()),
      fetch("http://localhost:8000/api/v1/doctors/").then((res) => res.json()),
    ]).then(([examsData, patientsData, examTypesData, doctorsData]) => {
      setExams(Array.isArray(examsData) ? examsData : []);
      setPatients(Array.isArray(patientsData) ? patientsData : []);
      setExamTypes(Array.isArray(examTypesData) ? examTypesData : []);
      setDoctors(Array.isArray(doctorsData) ? doctorsData : []);
      setLoading(false);
    });
  }, []);

  const patientMap = Object.fromEntries(patients.map((p) => [p.id, p.name]));
  const examTypeMap = Object.fromEntries(examTypes.map((et) => [et.id, et.name]));
  const doctorMap = Object.fromEntries(doctors.map((d) => [d.id, d.name]));
  const examsArray = Array.isArray(exams) ? exams : [];

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Exams</h1>
        <Link href="/exames/novo" className="bg-blue-600 text-white px-4 py-2 rounded">New Exam</Link>
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : examsArray.length === 0 ? (
        <p>No exams found.</p>
      ) : (
        <table className="min-w-full border">
          <thead>
            <tr>
              <th className="border px-2 py-1">Patient</th>
              <th className="border px-2 py-1">Date</th>
              <th className="border px-2 py-1">Exam Types</th>
              <th className="border px-2 py-1">Doctor</th>
              <th className="border px-2 py-1">Lab</th>
              <th className="border px-2 py-1">Results</th>
            </tr>
          </thead>
          <tbody>
            {examsArray.map((e, idx) => (
              <tr key={e.id || idx}>
                <td className="border px-2 py-1">{patientMap[e.patient_id] || e.patient_id}</td>
                <td className="border px-2 py-1">{new Date(e.test_date).toLocaleDateString()}</td>
                <td className="border px-2 py-1">{e.exam_types.map((etid) => examTypeMap[etid] || etid).join(", ")}</td>
                <td className="border px-2 py-1">{doctorMap[e.doctor_id || ""] || e.doctor_id || "-"}</td>
                <td className="border px-2 py-1">{e.lab_name}</td>
                <td className="border px-2 py-1">
                  {Array.isArray(e.results) && e.results.length > 0 ? (
                    <ul>
                      {e.results.map((r: any, i: number) => (
                        <li key={i}>
                          {examTypeMap[r.exam_type_id] || r.exam_type_id}: {r.value}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <span>-</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
} 