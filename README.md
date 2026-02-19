# MuleRift

A graph-based financial intelligence tool that detects money muling patterns from transaction data using cycle detection and temporal velocity analysis.

## Live Demo

Upload your transaction CSV file or run the sample data to see suspicious rings detected in real-time.

## Tech Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Visualization**: D3.js force-directed graph
- **Backend**: Python 3.x with NetworkX for graph analysis
- **Data Processing**: Pandas for CSV parsing

## Detection Algorithms

MuleRift models transactions as a directed graph where accounts are nodes and transactions are directed edges. The system identifies suspicious patterns through:

1. **Cycle Detection** - Identifies rings where funds flow through multiple accounts and return to the origin (A → B → C → A)
2. **Temporal Velocity Analysis** - Detects rapid pass-through transactions where funds move through an account within 72 hours
3. **Suspicion Scoring** - Combines structural (cycle participation) and temporal (velocity) signals into a weighted score (0-100)

Each cycle becomes a "ring" with an aggregated suspicion score based on member account behavior.

## Setup

### Prerequisites

- Node.js 18+
- Python 3.8+

### Installation

```bash
# Install Node dependencies
npm install

# Install Python dependencies
pip install -r python-engine/requirements.txt

# Run development server
npm run dev
```

Visit `http://localhost:3000` to use the application.

## CSV Format

Your CSV should include these columns:
- `from_account` - Source account identifier
- `to_account` - Destination account identifier
- `amount` - Transaction amount (numeric)
- `timestamp` - Transaction timestamp (ISO 8601 format)

## API Endpoints

- `POST /api/analyze` - Upload CSV for analysis
- `POST /api/sample` - Run analysis on sample data
- `POST /api/download` - Download results as JSON
- `GET /api/health` - Health check

## Project Structure

```
mulerift/
├── app/                    # Next.js App Router
├── components/             # React components
├── lib/                    # TypeScript utilities
├── python-engine/          # Python graph analysis engine
├── public/                 # Static assets
└── README.md
```
