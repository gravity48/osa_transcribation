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


export {Connections}
