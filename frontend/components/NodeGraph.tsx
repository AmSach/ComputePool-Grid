import React, { useMemo } from 'react';
import { Cpu, Activity } from 'lucide-react';

const NodeGraph = () => {
    // Simulated network node coordinates
    const nodes = useMemo(() => {
        return [...Array(12)].map((_, i) => ({
            id: i,
            x: Math.random() * 100,
            y: Math.random() * 100,
            status: Math.random() > 0.2 ? 'online' : 'warning',
            load: Math.floor(Math.random() * 100)
        }));
    }, []);

    return (
        <div className="bg-black border-2 border-zinc-800 rounded-xl p-6 h-[400px] relative overflow-hidden group">
            <div className="absolute top-4 left-4 z-10">
                <h3 className="text-zinc-500 text-[10px] uppercase font-bold tracking-[0.2em] mb-1">Network Topology</h3>
                <div className="flex items-center gap-2">
                    <Activity className="w-4 h-4 text-green-500 animate-pulse" />
                    <span className="text-white text-sm font-mono tracking-tighter">FLEET_SYNC: 99.8%</span>
                </div>
            </div>

            <svg className="w-full h-full opacity-40">
                {/* Connect nodes with lines */}
                {nodes.map((node, i) => (
                    nodes.slice(i + 1, i + 3).map((target, j) => (
                        <line 
                            key={`${i}-${j}`}
                            x1={`${node.x}%`} 
                            y1={`${node.y}%`} 
                            x2={`${target.x}%`} 
                            y2={`${target.y}%`} 
                            stroke="#1e1e1e" 
                            strokeWidth="1"
                        />
                    ))
                ))}
            </svg>

            {nodes.map((node) => (
                <div 
                    key={node.id}
                    className="absolute w-3 h-3 transform -translate-x-1/2 -translate-y-1/2 group-hover:scale-150 transition-transform cursor-pointer"
                    style={{ left: `${node.x}%`, top: `${node.y}%` }}
                >
                    <div className={`w-full h-full rounded-full ${node.status === 'online' ? 'bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]' : 'bg-yellow-500 animate-ping'}`} />
                    <div className="absolute hidden hover:block bg-zinc-900 border border-zinc-700 p-2 text-[8px] whitespace-nowrap z-50 mt-2 rounded">
                        ID: NODE-{node.id} | LOAD: {node.load}%
                    </div>
                </div>
            ))}

            <div className="absolute bottom-4 right-4 text-[10px] text-zinc-600 font-mono">
                COMPUTE_POOL_MESH_V4.2
            </div>
        </div>
    );
};

export default NodeGraph;
