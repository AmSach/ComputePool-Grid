"use client";
import { useState, useEffect } from "react";
import { getStatus, getNodes, getJobs } from "../lib/api";

export default function Dashboard() {
  const [status, setStatus] = useState<any>(null);
  const [nodes, setNodes] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [s, n, j] = await Promise.all([getStatus(), getNodes(), getJobs()]);
        setStatus(s);
        setNodes(n.nodes || []);
        setJobs(j.jobs || []);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl font-mono font-bold text-cyan-400 animate-pulse">INITIALIZING POOL...</div>
          <div className="mt-4 text-gray-500">Connecting to ComputePool network</div>
        </div>
      </div>
    );
  }

  const onlineNodes = nodes.filter((n: any) => n.online);

  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      {/* Hero */}
      <div className="text-center py-16">
        <h1 className="text-6xl font-mono font-black tracking-tight mb-4">
          <span className="text-cyan-400">Power</span> the{" "}
          <span className="text-white">Grid</span>
        </h1>
        <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-8">
          Decentralized compute. Share your GPU, earn credits, access unlimited power.
          Built like BitTorrent — for compute.
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="/pool"
            className="px-8 py-4 bg-cyan-500 hover:bg-cyan-400 text-black font-bold rounded-lg transition"
          >
            Join the Pool
          </a>
          <a
            href="/jobs"
            className="px-8 py-4 bg-white/10 hover:bg-white/20 text-white font-bold rounded-lg border border-white/20 transition"
          >
            Submit a Job
          </a>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
        {[
          { label: "Total Nodes", value: status?.nodes || 0, color: "text-cyan-400" },
          { label: "Online Now", value: onlineNodes.length, color: "text-green-400" },
          { label: "Jobs Run", value: status?.jobs || 0, color: "text-purple-400" },
          { label: "Network Status", value: "LIVE", color: "text-green-500" },
        ].map((stat) => (
          <div
            key={stat.label}
            className="bg-white/5 border border-white/10 rounded-xl p-6 text-center"
          >
            <div className={`text-4xl font-mono font-black ${stat.color}`}>{stat.value}</div>
            <div className="text-gray-500 text-sm mt-1">{stat.label}</div>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Live Nodes */}
        <div className="bg-white/5 border border-white/10 rounded-xl p-6">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            Active Nodes
          </h2>
          {onlineNodes.length === 0 ? (
            <div className="text-gray-500 text-center py-8">No nodes online. Be the first to join!</div>
          ) : (
            <div className="space-y-3">
              {onlineNodes.map((n: any) => (
                <div key={n.id} className="flex items-center justify-between bg-black/30 rounded-lg px-4 py-3">
                  <div>
                    <div className="font-mono text-sm font-bold">{n.name}</div>
                    <div className="text-xs text-gray-500">{n.gpuTier} · {n.cpuCores} cores · {n.ramGb}GB RAM</div>
                  </div>
                  <div className="text-right">
                    <div className="text-cyan-400 font-mono text-sm">{n.qualityScore}x</div>
                    <div className="text-xs text-gray-500">{n.region?.toUpperCase()}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Jobs */}
        <div className="bg-white/5 border border-white/10 rounded-xl p-6">
          <h2 className="text-xl font-bold mb-4">Recent Jobs</h2>
          {jobs.length === 0 ? (
            <div className="text-gray-500 text-center py-8">No jobs yet.</div>
          ) : (
            <div className="space-y-3">
              {jobs.slice(0, 6).map((j: any) => (
                <div key={j.id} className="flex items-center justify-between bg-black/30 rounded-lg px-4 py-3">
                  <div>
                    <div className="font-mono text-sm font-bold">{j.id}</div>
                    <div className="text-xs text-gray-500">{j.type} · {j.status}</div>
                  </div>
                  <div className={`text-sm font-bold ${j.status === "completed" ? "text-green-400" : j.status === "failed" ? "text-red-400" : "text-yellow-400"}`}>
                    {j.status}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* How it works */}
      <div className="mt-16 text-center">
        <h2 className="text-2xl font-bold mb-8">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { step: "01", title: "Install Node Agent", desc: "One command to install. Works on any OS, any GPU." },
            { step: "02", title: "Share & Earn", desc: "Your idle compute earns credits you can spend or cash out." },
            { step: "03", title: "Submit Jobs", desc: "ML training, rendering, gaming — any compute task, at a fraction of the cost." },
          ].map((item) => (
            <div key={item.step} className="bg-white/5 border border-white/10 rounded-xl p-6">
              <div className="text-4xl font-mono font-black text-cyan-400/30 mb-4">{item.step}</div>
              <h3 className="font-bold text-lg mb-2">{item.title}</h3>
              <p className="text-gray-400 text-sm">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}