import React, { useState } from 'react';
import { ShoppingCart, Server, Zap, DollarSign } from 'lucide-react';

const Marketplace = () => {
    const [offers] = useState([
        { id: 'node-01', provider: 'H100-Cluster', vram: '80GB', price: '$2.50/hr', region: 'us-east' },
        { id: 'node-02', provider: 'RTX-4090-Home', vram: '24GB', price: '$0.45/hr', region: 'eu-west' },
        { id: 'node-03', provider: 'A100-Instance', vram: '40GB', price: '$1.20/hr', region: 'asia-south' },
    ]);

    return (
        <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-6 text-white shadow-2xl">
            <div className="flex items-center gap-3 mb-6 border-b border-zinc-800 pb-4">
                <ShoppingCart className="text-blue-500 w-6 h-6" />
                <h2 className="text-2xl font-bold tracking-tight">Compute Spot Marketplace</h2>
            </div>
            
            <div className="grid gap-4">
                {offers.map((offer) => (
                    <div key={offer.id} className="flex items-center justify-between p-4 bg-zinc-950 border border-zinc-800 rounded-md hover:border-blue-500/50 transition-all group">
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-zinc-900 rounded-full group-hover:bg-blue-900/20 transition-colors">
                                <Server className="w-5 h-5 text-zinc-400 group-hover:text-blue-400" />
                            </div>
                            <div>
                                <p className="font-semibold text-zinc-100">{offer.provider}</p>
                                <p className="text-xs text-zinc-500 uppercase tracking-widest">{offer.region} // {offer.vram}</p>
                            </div>
                        </div>
                        
                        <div className="flex items-center gap-6">
                            <div className="text-right">
                                <p className="text-lg font-mono font-bold text-green-400">{offer.price}</p>
                                <p className="text-[10px] text-zinc-600">Dynamic pricing enabled</p>
                            </div>
                            <button className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-sm font-bold rounded-sm transition-colors flex items-center gap-2">
                                <Zap className="w-4 h-4" /> DEPLOY
                            </button>
                        </div>
                    </div>
                ))}
            </div>
            
            <div className="mt-6 flex justify-between items-center text-[10px] text-zinc-500 italic">
                <span>* Prices subject to node availability and network congestion</span>
                <span className="flex items-center gap-1"><DollarSign className="w-3 h-3" /> Minimum deposit: 5.00 CR</span>
            </div>
        </div>
    );
};

export default Marketplace;
