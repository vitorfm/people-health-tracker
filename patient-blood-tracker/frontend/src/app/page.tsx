import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <h1 className="text-3xl font-bold mb-8">People Health Tracker</h1>
      <div className="flex gap-4">
        <Link href="/pacientes" className="bg-blue-600 text-white px-6 py-3 rounded text-lg">Patients</Link>
        <Link href="/exames" className="bg-green-600 text-white px-6 py-3 rounded text-lg">Exams</Link>
        <Link href="/exam-types" className="bg-purple-600 text-white px-6 py-3 rounded text-lg">Exam Types</Link>
        <Link href="/doctors" className="bg-pink-600 text-white px-6 py-3 rounded text-lg">Doctors</Link>
      </div>
    </main>
  );
}
