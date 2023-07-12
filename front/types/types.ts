interface Connections{
  id: number,
  alias: string,
  ip: string,
  port: number,
  db_login: string,
  db_password: string,
  db_name: string,
  created_at: Date,
  options: Object,
  db_system: number,
  db_status: number | string
}

interface ConnectionStatus{
  id: number,
  status_name: string
}

interface ConnectionSystem{
  id: number,
  name: string
}

interface RecognizeServer{
  id: number,
  name: string,
  short_name: string,
  ip: string,
  port: number
}

interface TaskType{
  id: number,
  name: string
}

interface TaskStatus{
  id: number,
  status: string
}

interface Task{
  id: number,
  alias: string,
  db: number | string
  thread_count?: number,
  task_type?: string,
  status?: string,
  model?: number,
  period_from?: Date,
  period_to?: Date,
  options: Object,
  created_at?: Date,
}



export {
  Connections,
  ConnectionStatus,
  ConnectionSystem,
  Task,
  TaskStatus,
  RecognizeServer
}
