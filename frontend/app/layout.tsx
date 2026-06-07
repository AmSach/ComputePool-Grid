import type { Metadata } from "next";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "Sarva — Decentralized Compute Grid",
  description: "Share compute, earn credits, unlock unlimited power",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-[#0a0a0f] text-white font-sans antialiased">
        <nav className="fixed top-0 left-0 right-0 z-50 bg-black/60 backdrop-blur-md border-b border-white/10">
          <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
            <span className="text-xl font-mono font-bold tracking-tight">
              <span className="text-cyan-400">Compute</span>
              <span className="text-white">Pool</span>
            </span>
            <div className="flex gap-6 text-sm text-gray-400">
              <a href="/" className="hover:text-white transition">Dashboard</a>
              <a href="/nodes" className="hover:text-white transition">Nodes</a>
              <a href="/jobs" className="hover:text-white transition">Jobs</a>
              <a href="/credits" className="hover:text-white transition">Credits</a>
              <a href="/pool" className="hover:text-white transition">Join Pool</a>
            </div>
          </div>
        </nav>
        <main className="pt-20">{children}</main>
      </body>
    </html>
  );
}