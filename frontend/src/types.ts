export interface DailyLog {
  id: number;
  date: string;
  water_liters: number;
  meals_count: number;
  sugar_grams: number;
  sleep_hours: number;
  work_hours: number;
  mood: number;
}

export interface DailyLogCreate {
  date?: string;
  water_liters: number;
  meals_count: number;
  sugar_grams: number;
  sleep_hours: number;
  work_hours: number;
  mood: number;
}