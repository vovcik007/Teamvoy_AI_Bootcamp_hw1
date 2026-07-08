import axios from 'axios';
import type { DailyLog, DailyLogCreate } from './types';
import type { HealthStats } from './types';

const API = axios.create({
  baseURL: 'http://localhost:8000',
});

export const fetchLogs = async (): Promise<DailyLog[]> => {
  const response = await API.get('/logs/');
  return response.data;
};

export const saveLog = async (data: DailyLogCreate): Promise<DailyLog> => {
  const response = await API.post('/logs/', data);
  return response.data;
};

export const fetchStats = async (): Promise<HealthStats> => {
  const response = await API.get('/stats/');
  return response.data;
};
