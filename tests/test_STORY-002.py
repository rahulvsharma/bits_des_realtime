import pytest
from datetime import datetime

class MockStockUpdate:
    def __init__(self, symbol, price, change_percent):
        self.symbol = symbol
        self.price = price
        self.timestamp = datetime.now()
        self.change_percent = change_percent

@pytest.fixture
def sample_stock_updates():
    return [
        MockStockUpdate("AAPL", 155.0, 2.5),
        MockStockUpdate("GOOGL", 2850.0, -1.2),
        MockStockUpdate("MSFT", 310.0, 1.8),
    ]

def test_stock_update_creation(sample_stock_updates):
    assert len(sample_stock_updates) == 3
    assert sample_stock_updates[0].symbol == "AAPL"

def test_stock_price_validation(sample_stock_updates):
    for stock in sample_stock_updates:
        assert stock.price > 0

def test_stock_change_percent(sample_stock_updates):
    positive_change = [s for s in sample_stock_updates if s.change_percent > 0]
    negative_change = [s for s in sample_stock_updates if s.change_percent < 0]
    assert len(positive_change) == 2
    assert len(negative_change) == 1

def test_websocket_message_format():
    stock = MockStockUpdate("AAPL", 155.0, 2.5)
    data = {
        "symbol": stock.symbol,
        "price": stock.price,
        "timestamp": stock.timestamp.isoformat(),
        "change_percent": stock.change_percent
    }
    assert "symbol" in data
    assert "price" in data
    assert "timestamp" in data
