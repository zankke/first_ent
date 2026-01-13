# 통합 인증 설정 가이드

## 개요

Supabase 로그인과 시스템 사용자 계정(Account)을 이메일 기반으로 통합한 인증 시스템입니다.

## 아키텍처

```
┌─────────────────┐         ┌──────────────────┐
│ Supabase 로그인  │  ────>  │ 시스템 사용자 계정 │
│                 │         │                  │
│ - 이메일/비밀번호 │  이메일  │ - 권한 (level)    │
│ - 세션 관리      │  매칭   │ - 상태 (status)   │
│ - JWT 토큰      │         │ - 역할 관리        │
└─────────────────┘         └──────────────────┘
         │                           │
         └───────────┬───────────────┘
                     │
              ┌──────▼──────┐
              │  권한 확인   │
              │  미들웨어    │
              └─────────────┘
```

## 설정 단계

### 1. 백엔드 환경 변수 설정

`backend/.env` 파일에 다음을 추가:

```env
# Supabase 설정
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here

# 기존 설정 유지
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=first_ent
```

### 2. 프론트엔드 환경 변수 설정

`frontend/.env` 파일에 다음을 추가:

```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

### 3. 의존성 설치

**백엔드:**
```bash
cd backend
source venv/bin/activate
pip install PyJWT
```

**프론트엔드:**
```bash
cd frontend
npm install  # 이미 설치됨
```

### 4. 데이터베이스에 계정 생성

Supabase에서 회원가입한 사용자의 이메일로 Account를 생성해야 합니다:

```sql
INSERT INTO Users (uid, uemail, upass, level, status) 
VALUES ('admin', 'user@example.com', '$2b$12$...', 'admin', 'Y');
```

또는 백엔드 API 사용:
```bash
POST /api/accounts/
{
  "username": "admin",
  "email": "user@example.com",  # Supabase 이메일과 일치해야 함
  "password": "password",
  "role": "admin"
}
```

## 사용 방법

### 1. 사용자 로그인 플로우

1. 사용자가 `/login`에서 Supabase로 로그인
2. 로그인 성공 시 Supabase JWT 토큰 발급
3. 프론트엔드가 토큰을 `Authorization: Bearer <token>` 헤더에 포함
4. 백엔드가 토큰에서 이메일 추출
5. 이메일로 Account 조회 및 권한 확인
6. 권한에 따라 API 접근 허용/거부

### 2. 권한 레벨

- **admin**: 모든 권한 (생성, 수정, 삭제)
- **manager**: 생성, 수정 권한
- **viewer**: 조회 전용 권한

### 3. API 엔드포인트 보호

```python
from backend.utils.auth import require_auth, require_role

@bp.route('/protected', methods=['GET'])
@require_auth  # 인증 필요
def protected_route():
    # g.current_user: Account 객체
    # g.user_email: 사용자 이메일
    # g.user_level: 권한 레벨
    return jsonify({'message': 'Success'})

@bp.route('/admin-only', methods=['POST'])
@require_role('admin')  # admin 권한만
def admin_route():
    return jsonify({'message': 'Admin only'})
```

### 4. 프론트엔드에서 권한 확인

```typescript
const { account, level, permissions } = useContext(AuthContext);

if (permissions?.can_create) {
  // 생성 버튼 표시
}

if (level === 'admin') {
  // 관리자 메뉴 표시
}
```

## API 엔드포인트

### 인증 관련

- `GET /api/auth/me` - 현재 사용자 정보 및 권한 조회
- `POST /api/auth/verify` - 토큰 검증 및 권한 확인

### 계정 관리 (권한 필요)

- `GET /api/accounts/` - 계정 목록 (인증 필요)
- `POST /api/accounts/` - 계정 생성 (admin만)
- `PUT /api/accounts/<id>` - 계정 수정 (admin, manager)
- `DELETE /api/accounts/<id>` - 계정 삭제 (admin만)

## 문제 해결

### 1. "시스템에 등록되지 않은 사용자입니다" 오류

**원인**: Supabase에 로그인했지만 Account 테이블에 해당 이메일이 없음

**해결**: 
- Account를 생성하거나
- 기존 Account의 `uemail`을 Supabase 이메일과 일치시킴

### 2. "비활성화된 계정입니다" 오류

**원인**: Account의 `status`가 'N'임

**해결**: 
```sql
UPDATE Users SET status = 'Y' WHERE uemail = 'user@example.com';
```

### 3. 토큰 검증 실패

**원인**: Supabase URL/키가 잘못 설정됨

**해결**: `.env` 파일의 Supabase 설정 확인

## 보안 고려사항

1. **토큰 검증**: 모든 보호된 엔드포인트에서 토큰 검증 수행
2. **권한 확인**: 각 작업 전에 권한 레벨 확인
3. **이메일 매칭**: Supabase 이메일과 Account 이메일이 정확히 일치해야 함
4. **상태 확인**: Account의 `status`가 'Y'인지 확인

## 개발 모드

개발 환경(`FLASK_ENV=development`)에서는:
- 토큰 검증 실패 시 테스트용 이메일 허용
- 네트워크 오류 시에도 계속 진행 가능

**주의**: 프로덕션 환경에서는 반드시 실제 토큰 검증이 필요합니다.

