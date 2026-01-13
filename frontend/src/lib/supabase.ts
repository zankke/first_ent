import { createClient } from '@supabase/supabase-js'

const supabaseUrl = (import.meta.env as any).VITE_SUPABASE_URL
const supabaseAnonKey = (import.meta.env as any).VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  const errorMessage = `
  ⚠️ Supabase 환경 변수가 설정되지 않았습니다!
  
  다음 단계를 따라주세요:
  1. frontend/.env 파일을 생성하세요
  2. 다음 내용을 추가하세요:
  
     VITE_SUPABASE_URL=https://your-project-id.supabase.co
     VITE_SUPABASE_ANON_KEY=your-anon-key-here
  
  3. Supabase 프로젝트 이름: common_login
  4. Supabase 대시보드 > 프로젝트 설정 > API에서 URL과 키를 가져오세요
  5. 개발 서버를 재시작하세요 (npm run dev)
  `
  console.error(errorMessage)
  throw new Error('VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY must be set in .env file. See console for details.')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

