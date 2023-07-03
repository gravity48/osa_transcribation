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
  db_status: number
}

interface ConnectionStatus{
  id: number,
  status_name: string
}

interface ConnectionSystem{
  id: number,
  name: string
}

export {Connections, ConnectionStatus, ConnectionSystem}
