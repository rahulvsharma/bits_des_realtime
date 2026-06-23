import React, { useEffect, useState } from 'react';

interface StockUpdate {
  symbol: string;
  price: number;
  timestamp: string;
  change_percent: number;
}

export const RealtimeStockComponent: React.FC = () => {
  const [stocks, setStocks] = useState<StockUpdate[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws/stock-stream');
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStocks(prev => [...prev, data]);
    };
    setWs(websocket);
    return () => websocket.close();
  }, []);

  return (
    <div className="realtime-stock p-6">
      <h1 className="text-2xl font-bold mb-4">Real-time Stock Updates</h1>
      <div className="grid grid-cols-1 gap-4">
        {stocks.map((stock, idx) => (
          <div key={idx} className="border p-4 rounded bg-white shadow">
            <p className="font-bold">{stock.symbol}</p>
            <p className="text-lg">${stock.price}</p>
            <p className={stock.change_percent >= 0 ? 'text-green-600' : 'text-red-600'}>
              {stock.change_percent >= 0 ? '+' : ''}{stock.change_percent}%
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RealtimeStockComponent;
