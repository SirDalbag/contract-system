export interface IData {
  id: number
  total: string
  date: string
  file_path: string
  author: number
  agent_id: number
  comment_id: number
  username: string
}

export interface IForm {
  bin: string;
  comment: string;
  total: number;
  file_path: File | null;
}
