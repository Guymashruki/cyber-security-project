import React, { useState, useEffect, useRef, useMemo } from 'react';
import Chart from 'chart.js/auto';

// --- רכיב כרטיס סטטיסטיקה ---
const StatCard = ({ title, value, color }) => (
    <div className={`bg-white p-6 rounded-xl shadow-sm border-l-4 ${color} transition hover:shadow-md`}>
        <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">{title}</p>
        <h3 className="text-3xl font-extrabold text-slate-900 mt-2">{value}</h3>
    </div>
);

// --- הרכיב הראשי ---
const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const chartRef = useRef(null);
    const chartInstance = useRef(null);

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:8080/reports');
            const reports = await response.json();
            if (reports.length > 0) {
                const latest = JSON.parse(reports[reports.length - 1].content);
                setData(latest);
            }
        } catch (err) {
            console.error("Fetch error:", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const filteredAnomalies = useMemo(() => {
        if (!data || !data.anomalies) return [];
        
        return data.anomalies.filter(item => {
            const ip = item.ip || item.ip_address || item.source_ip || item.src_ip || item.IP || "";
            const user = item.user_id || "";
            const reason = item.reason || "";
            
            return ip.includes(searchTerm) || 
                   user.toLowerCase().includes(searchTerm.toLowerCase()) ||
                   reason.toLowerCase().includes(searchTerm.toLowerCase());
        });
    }, [data, searchTerm]);

    // --- יצירת הגרף ---
    useEffect(() => {
        if (data && data.anomalies && chartRef.current) {
            
            const counts = {};
            data.anomalies.forEach(a => {
                const fullReason = a.reason || "Unknown";
                const shortReason = fullReason.split(':')[0]; 
                counts[shortReason] = (counts[shortReason] || 0) + 1;
            });

            const labels = Object.keys(counts);
            const values = Object.values(counts);

            const backgroundColors = labels.map(label => {
                const l = label.toLowerCase();
                if (l.includes("brute")) return '#f59e0b';      
                if (l.includes("geo")) return '#8b5cf6';        
                if (l.includes("suspicious")) return '#ef4444'; 
                return '#cbd5e1'; 
            });

            if (chartInstance.current) chartInstance.current.destroy();

            const ctx = chartRef.current.getContext('2d');
            chartInstance.current = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: backgroundColors, 
                        borderWidth: 0
                    }]
                },
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false, 
                    plugins: { legend: { position: 'right' } }
                }
            });
        }
        
        // ניקוי ביציאה
        return () => {
            if (chartInstance.current) chartInstance.current.destroy();
        };
    }, [data]);

    const getReasonStyle = (reason) => {
        if (!reason) return "bg-gray-100 text-gray-700";
        if (reason.toLowerCase().includes("brute")) return "bg-amber-100 text-amber-700 border border-amber-200";
        if (reason.toLowerCase().includes("geo")) return "bg-purple-100 text-purple-700 border border-purple-200";
        if (reason.toLowerCase().includes("suspicious")) return "bg-rose-100 text-rose-700 border border-rose-200";
        return "bg-slate-100 text-slate-700";
    };

    if (loading) return (
        <div className="flex h-screen items-center justify-center bg-slate-50">
            <div className="text-center">
                <div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <p className="text-indigo-900 font-semibold">Loading Security Data...</p>
            </div>
        </div>
    );

    return (
        <div className="min-h-screen p-8 max-w-7xl mx-auto bg-slate-50 text-slate-800 font-sans">
            <div className="flex flex-col md:flex-row justify-between items-center mb-10 gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-2">
                        🛡️ RSecurity <span className="text-indigo-600">Intelligence</span>
                    </h1>
                    <p className="text-slate-500 text-sm mt-1">Real-time Anomaly Detection System</p>
                </div>
                <button 
                    onClick={fetchData}
                    className="bg-slate-900 hover:bg-slate-800 text-white px-6 py-2.5 rounded-lg font-medium transition-all shadow-lg shadow-slate-200 flex items-center gap-2"
                >
                    <span>🔄</span> Refresh Data
                </button>
            </div>

            {!data ? (
                <div className="bg-amber-50 border border-amber-200 p-6 rounded-xl text-amber-800 text-center">
                    <p className="font-bold">No data found on server.</p>
                    <p className="text-sm mt-2">Please run client.py to upload data.</p>
                </div>
            ) : (
                <>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                        <StatCard title="Total Logs Scanned" value={data.summary.total_logs} color="border-indigo-500" />
                        <StatCard title="Threats Detected" value={data.summary.anomalies_found} color="border-rose-500" />
                        <StatCard 
                            title="System Status" 
                            value={data.summary.anomalies_found > 0 ? "COMPROMISED" : "SECURE"} 
                            color={data.summary.anomalies_found > 0 ? "border-rose-500 text-rose-600" : "border-emerald-500 text-emerald-600"} 
                        />
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div className="bg-white p-6 rounded-2xl shadow-sm lg:col-span-1">
                            <h2 className="text-lg font-bold text-slate-800 mb-6">Attack Distribution</h2>
                            <div className="h-64 relative">
                                <canvas ref={chartRef}></canvas>
                            </div>
                        </div>

                        <div className="bg-white p-6 rounded-2xl shadow-sm lg:col-span-2 flex flex-col">
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-lg font-bold text-slate-800">Live Anomalies Feed</h2>
                                <input 
                                    type="text" 
                                    placeholder="🔍 Filter by User, IP or Type..." 
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="border border-slate-200 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 w-64"
                                />
                            </div>

                            <div className="overflow-x-auto flex-grow">
                                <table className="w-full text-left border-collapse">
                                    <thead>
                                        <tr className="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-100">
                                            <th className="pb-3 pl-2 w-32">Time</th>
                                            <th className="pb-3 w-32">User</th>
                                            <th className="pb-3 w-40">Attacker IP</th>
                                            <th className="pb-3">Identification / Reason</th>
                                        </tr>
                                    </thead>
                                    <tbody className="text-sm divide-y divide-slate-50">
                                        {filteredAnomalies.length > 0 ? (
                                            filteredAnomalies.map((item, index) => (
                                                <tr key={index} className="hover:bg-slate-50 transition-colors">
                                                    <td className="py-3 pl-2 text-slate-500 font-mono text-xs whitespace-nowrap">{(item.timestamp || "").split(' ')[1]}</td>
                                                    <td className="py-3 font-semibold text-slate-700">{item.user_id || "Unknown"}</td>
                                                    <td className="py-3 font-mono text-indigo-600 font-medium">{item.ip || item.ip_address || item.source_ip || "N/A"}</td>
                                                    <td className="py-3">
                                                        <div className={`px-3 py-2 rounded-lg text-xs font-medium inline-block w-full ${getReasonStyle(item.reason)}`}>
                                                            {item.reason || "Unknown"}
                                                        </div>
                                                    </td>
                                                </tr>
                                            ))
                                        ) : (
                                            <tr>
                                                <td colSpan="4" className="text-center py-8 text-slate-400 italic">No results match "{searchTerm}"</td>
                                            </tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default Dashboard;