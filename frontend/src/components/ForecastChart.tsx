import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine, Legend
} from 'recharts'
import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { getRevenueForecast } from '../api/orders'
import type { RevenueForecast, ForecastPoint } from '../types'

export default function ForecastChart() {
  const [days, setDays] = useState<number>(30)

  const { data, isLoading, error } = useQuery<RevenueForecast>({
    queryKey: ['forecast', days],
    queryFn: () => getRevenueForecast(days),
  })

  if (isLoading) return (
    <div className="text-center py-5">
      <div className="spinner-border spinner-border-sm" />
      <span className="ms-2 text-muted">Running forecast model...</span>
    </div>
  )

  if (error || data?.error) return (
    <div className="alert alert-warning">
      {data?.error || 'Failed to load forecast. Make sure you have enough order history.'}
    </div>
  )

  if (!data) return null

  // Merge historical and forecast into one dataset for the chart
  const historical = data.historical.map((p: ForecastPoint) => ({
    date: p.date,
    historical: p.revenue,
    forecast: null,
  }))

  const forecastData = data.forecast.map((p: ForecastPoint) => ({
    date: p.date,
    historical: null,
    forecast: p.revenue,
  }))

  const chartData = [...historical, ...forecastData]
  const forecastStartDate = data.summary.forecast_start

  return (
    <div className="card shadow-sm">
      <div className="card-body p-4">

        {/* Header */}
        <div className="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h5 className="mb-0">Revenue Forecast</h5>
            <small className="text-muted">
              Powered by scikit-learn · LinearRegression + Polynomial features
            </small>
          </div>
          <select
            className="form-select form-select-sm"
            style={{ width: 140 }}
            value={days}
            onChange={e => setDays(Number(e.target.value))}
          >
            <option value={7}>Next 7 days</option>
            <option value={30}>Next 30 days</option>
            <option value={60}>Next 60 days</option>
            <option value={90}>Next 90 days</option>
          </select>
        </div>

        {/* Summary KPIs */}
        <div className="row g-2 mb-4">
          <div className="col-4">
            <div className="bg-light rounded p-3 text-center">
              <div className="text-muted" style={{ fontSize: 12 }}>Forecast revenue</div>
              <div className="fw-bold fs-5">
                ₱{data.summary.total_forecast_revenue.toLocaleString()}
              </div>
            </div>
          </div>
          <div className="col-4">
            <div className="bg-light rounded p-3 text-center">
              <div className="text-muted" style={{ fontSize: 12 }}>Daily average</div>
              <div className="fw-bold fs-5">
                ₱{data.summary.avg_daily_revenue.toLocaleString()}
              </div>
            </div>
          </div>
          <div className="col-4">
            <div className="bg-light rounded p-3 text-center">
              <div className="text-muted" style={{ fontSize: 12 }}>Period</div>
              <div className="fw-bold" style={{ fontSize: 13 }}>
                {data.summary.forecast_start} → {data.summary.forecast_end}
              </div>
            </div>
          </div>
        </div>

        {/* Chart */}
        <ResponsiveContainer width="100%" height={280}>
          <AreaChart data={chartData} margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
            <defs>
              <linearGradient id="historical-grad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#1D9E75" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#1D9E75" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="forecast-grad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#7F77DD" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#7F77DD" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 11 }}
              tickFormatter={d => d.slice(5)}
              interval="preserveStartEnd"
            />
            <YAxis
              tick={{ fontSize: 11 }}
              tickFormatter={v => `₱${v.toLocaleString()}`}
              width={80}
            />
            <Tooltip
              formatter={(value: number) => [`₱${value?.toLocaleString() ?? 0}`, '']}
              labelFormatter={label => `Date: ${label}`}
            />
            <Legend />
            <ReferenceLine
              x={forecastStartDate}
              stroke="#aaa"
              strokeDasharray="4 4"
              label={{ value: 'Forecast start', fontSize: 11, fill: '#888' }}
            />
            <Area
              type="monotone"
              dataKey="historical"
              stroke="#1D9E75"
              strokeWidth={2}
              fill="url(#historical-grad)"
              name="Historical"
              connectNulls
            />
            <Area
              type="monotone"
              dataKey="forecast"
              stroke="#7F77DD"
              strokeWidth={2}
              strokeDasharray="5 5"
              fill="url(#forecast-grad)"
              name="Forecast"
              connectNulls
            />
          </AreaChart>
        </ResponsiveContainer>

        <p className="text-muted mt-2 mb-0" style={{ fontSize: 12 }}>
          Dashed line = predicted values. Based on historical order patterns,
          day-of-week trends, and seasonal factors.
        </p>
      </div>
    </div>
  )
}