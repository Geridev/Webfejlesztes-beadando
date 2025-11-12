// Real REST API integration based on API documentation

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

// Helper function to get auth token
const getAuthToken = () => {
  return localStorage.getItem('token');
};

// Helper function to make authenticated requests
const fetchWithAuth = async (url: string, options: RequestInit = {}) => {
  const token = getAuthToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
};

// Type definitions
export interface Service {
  id: number;
  name: string;
  description: string;
  duration: number;
  price: number;
}

export interface Appointment {
  id: number;
  user_id: number;
  service_id: number;
  datetime: string;
  status: 'booked' | 'cancelled' | 'completed';
  service?: Service;
}

export interface User {
  id: number;
  username: string;
  email: string;
  role: 'user' | 'admin';
}

// Auth API - /auth endpoints
export const authAPI = {
  login: async (username: string, password: string) => {
    const response = await fetchWithAuth('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    return {
      token: response.access_token,
      user: response.user,
    };
  },

  register: async (username: string, email: string, password: string) => {
    await fetchWithAuth('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
    return { success: true };
  },

  logout: async () => {
    await fetchWithAuth('/auth/logout', {
      method: 'POST',
    });
  },
};

// Services API - /services endpoints
export const servicesAPI = {
  getAll: async (): Promise<Service[]> => {
    return fetchWithAuth('/services/');
  },

  create: async (service: Omit<Service, 'id'>): Promise<Service> => {
    return fetchWithAuth('/services/', {
      method: 'POST',
      body: JSON.stringify(service),
    });
  },

  update: async (id: number, service: Partial<Service>): Promise<Service> => {
    return fetchWithAuth(`/services/${id}`, {
      method: 'PUT',
      body: JSON.stringify(service),
    });
  },

  delete: async (id: number) => {
    return fetchWithAuth(`/services/${id}`, {
      method: 'DELETE',
    });
  },
};

// Appointments API - /appointments endpoints
export const appointmentsAPI = {
  getUserAppointments: async (): Promise<Appointment[]> => {
    // GET /appointments/ returns user's appointments or all for admin
    return fetchWithAuth('/appointments/');
  },

  getAll: async (): Promise<Appointment[]> => {
    // Admin endpoint - returns all appointments
    return fetchWithAuth('/appointments/');
  },

  create: async (appointment: { service_id: number; datetime: string }): Promise<Appointment> => {
    return fetchWithAuth('/appointments/', {
      method: 'POST',
      body: JSON.stringify(appointment),
    });
  },

  update: async (id: number, data: { datetime?: string; status?: string }): Promise<Appointment> => {
    return fetchWithAuth(`/appointments/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  delete: async (id: number) => {
    return fetchWithAuth(`/appointments/${id}`, {
      method: 'DELETE',
    });
  },

  // Helper method to cancel appointment
  cancel: async (id: number): Promise<Appointment> => {
    return appointmentsAPI.update(id, { status: 'cancelled' });
  },

  // Helper method to update status
  updateStatus: async (id: number, status: 'booked' | 'cancelled' | 'completed'): Promise<Appointment> => {
    return appointmentsAPI.update(id, { status });
  },
};

// Users API - /users endpoints
export const usersAPI = {
  getAll: async (): Promise<User[]> => {
    return fetchWithAuth('/users/');
  },

  getById: async (id: number): Promise<User> => {
    return fetchWithAuth(`/users/${id}`);
  },

  update: async (id: number, updates: Partial<User>): Promise<User> => {
    return fetchWithAuth(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  },

  delete: async (id: number) => {
    return fetchWithAuth(`/users/${id}`, {
      method: 'DELETE',
    });
  },
};