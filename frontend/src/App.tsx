import { useState, useEffect } from 'react';
import { fetchLogs, saveLog, fetchStats } from './api';
import type { DailyLog, DailyLogCreate, HealthStats } from './types';
import './App.css';

function App() {
  const [logs, setLogs] = useState<DailyLog[]>([]);
  const [stats, setStats] = useState<HealthStats | null>(null);
  const [form, setForm] = useState<DailyLogCreate>({
    date: new Date().toISOString().split('T')[0],
    water_liters: 0,
    meals_count: 0,
    sugar_grams: 0,
    sleep_hours: 0,
    work_hours: 0,
    mood: 5,
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [logsData, statsData] = await Promise.all([fetchLogs(), fetchStats()]);
      setLogs(logsData);
      setStats(statsData);
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await saveLog(form);
      await loadData();
      setForm({
        date: new Date().toISOString().split('T')[0],
        water_liters: 0,
        meals_count: 0,
        sugar_grams: 0,
        sleep_hours: 0,
        work_hours: 0,
        mood: 5,
      });
    } catch (error) {
      console.error('Failed to save log:', error);
    }
  };

  const getMoodLabel = (mood: number) => {
    if (mood >= 8) return 'Excellent';
    if (mood >= 6) return 'Good';
    if (mood >= 4) return 'Fair';
    return 'Poor';
  };

  const getMoodClass = (mood: number) => {
    if (mood >= 8) return 'mood-excellent';
    if (mood >= 6) return 'mood-good';
    if (mood >= 4) return 'mood-fair';
    return 'mood-poor';
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>Health Tracker</h1>
          <p className="subtitle">Monitor your daily wellness metrics</p>
        </div>
      </header>

      <main className="main">
        {/* --- NEW STATS SECTION --- */}
        {stats && stats.total_logs > 0 && (
          <section className="card stats-card">
            <div className="card-header">
              <h2>Health Insights</h2>
              <p className="card-description">Based on your {stats.total_logs} logged days</p>
            </div>
            
            <div className="stats-grid">
              <div className="stat-box">
                <span className="stat-label">Avg Mood</span>
                <span className="stat-value">{stats.avg_mood}<span className="stat-unit">/10</span></span>
              </div>
              <div className="stat-box">
                <span className="stat-label">Avg Sleep</span>
                <span className="stat-value">{stats.avg_sleep}<span className="stat-unit">hrs</span></span>
              </div>
              <div className="stat-box">
                <span className="stat-label">Avg Water</span>
                <span className="stat-value">{stats.avg_water}<span className="stat-unit">L</span></span>
              </div>
            </div>

            <div className="insight-box">
              <h3>Correlation Insight</h3>
              <p>{stats.insight}</p>
            </div>
          </section>
        )}
        {/* --- END NEW STATS SECTION --- */}

        <section className="card form-card">
          <div className="card-header">
            <h2>Daily Log Entry</h2>
            <p className="card-description">Record your health metrics for today</p>
          </div>
          
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group full-width">
              <label htmlFor="date">Date</label>
              <input
                id="date"
                type="date"
                max={new Date().toISOString().split('T')[0]}
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
              />
            </div>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="water">Water Intake</label>
                <div className="input-wrapper">
                  <input
                    id="water"
                    type="number"
                    step="0.1"
                    min="0"
                    value={form.water_liters}
                    onChange={(e) => setForm({ ...form, water_liters: parseFloat(e.target.value) || 0 })}
                    placeholder="0.0"
                  />
                  <span className="unit">L</span>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="meals">Meals</label>
                <div className="input-wrapper">
                  <input
                    id="meals"
                    type="number"
                    min="0"
                    value={form.meals_count}
                    onChange={(e) => setForm({ ...form, meals_count: parseInt(e.target.value) || 0 })}
                    placeholder="0"
                  />
                  <span className="unit">count</span>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="sugar">Sugar Intake</label>
                <div className="input-wrapper">
                  <input
                    id="sugar"
                    type="number"
                    step="0.1"
                    min="0"
                    value={form.sugar_grams}
                    onChange={(e) => setForm({ ...form, sugar_grams: parseFloat(e.target.value) || 0 })}
                    placeholder="0.0"
                  />
                  <span className="unit">g</span>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="sleep">Sleep Duration</label>
                <div className="input-wrapper">
                  <input
                    id="sleep"
                    type="number"
                    step="0.5"
                    min="0"
                    max="24"
                    value={form.sleep_hours}
                    onChange={(e) => setForm({ ...form, sleep_hours: parseFloat(e.target.value) || 0 })}
                    placeholder="0.0"
                  />
                  <span className="unit">hrs</span>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="work">Work Hours</label>
                <div className="input-wrapper">
                  <input
                    id="work"
                    type="number"
                    step="0.5"
                    min="0"
                    max="24"
                    value={form.work_hours}
                    onChange={(e) => setForm({ ...form, work_hours: parseFloat(e.target.value) || 0 })}
                    placeholder="0.0"
                  />
                  <span className="unit">hrs</span>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="mood">Mood Score</label>
                <div className="input-wrapper">
                  <input
                    id="mood"
                    type="number"
                    min="1"
                    max="10"
                    value={form.mood}
                    onChange={(e) => setForm({ ...form, mood: parseInt(e.target.value) || 5 })}
                    placeholder="5"
                  />
                  <span className="unit">/10</span>
                </div>
              </div>
            </div>

            <button type="submit" className="submit-btn">
              Save Entry
            </button>
          </form>
        </section>

        <section className="card history-card">
          <div className="card-header">
            <h2>Recent History</h2>
            <p className="card-description">Your health metrics over time</p>
          </div>
          
          {logs.length === 0 ? (
            <div className="empty-state">
              <p>No entries yet</p>
              <p className="empty-hint">Start tracking your health by filling out the form above</p>
            </div>
          ) : (
            <div className="table-wrapper">
              <table className="logs-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Water</th>
                    <th>Meals</th>
                    <th>Sugar</th>
                    <th>Sleep</th>
                    <th>Work</th>
                    <th>Mood</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map((log) => (
                    <tr key={log.id}>
                      <td className="date-cell">{new Date(log.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</td>
                      <td><span className="metric-value">{log.water_liters}</span><span className="metric-unit">L</span></td>
                      <td><span className="metric-value">{log.meals_count}</span></td>
                      <td><span className="metric-value">{log.sugar_grams}</span><span className="metric-unit">g</span></td>
                      <td><span className="metric-value">{log.sleep_hours}</span><span className="metric-unit">h</span></td>
                      <td><span className="metric-value">{log.work_hours}</span><span className="metric-unit">h</span></td>
                      <td>
                        <div className="mood-display">
                          <span className={`mood-badge ${getMoodClass(log.mood)}`}>
                            {log.mood}
                          </span>
                          <span className="mood-label">{getMoodLabel(log.mood)}</span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;