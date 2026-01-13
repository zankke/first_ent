# 인증 시스템 가이드

## 개요

현재 프로젝트에는 두 가지 인증 시스템이 존재합니다:

1. **Supabase 로그인 계정** - 프론트엔드 인증 (웹 앱 접근)
2. **시스템 사용자 계정** - 백엔드 권한 관리 (시스템 내부 권한)

---

## 1. Supabase 로그인 계정

### 용도
- **웹 애플리케이션 접근 인증**
- 사용자가 프론트엔드에 로그인하여 시스템에 접근
- 세션 관리 및 보안 토큰 처리

### 특징
- ✅ 이메일/비밀번호 기반 인증
- ✅ 자동 세션 관리
- ✅ 이메일 인증 기능
- ✅ 비밀번호 재설정 기능
- ✅ Supabase 클라우드에서 관리

### 저장 위치
- Supabase 인증 서버 (PostgreSQL)
- 로컬 데이터베이스에 저장되지 않음

### 사용 위치
```typescript
// 프론트엔드
- src/pages/Login.tsx      // 로그인 페이지
- src/pages/Signup.tsx     // 회원가입 페이지
- src/context/AuthContext.tsx  // 인증 상태 관리
```

### 접근 방법
1. 사용자가 웹 브라우저에서 `/login` 페이지 접근
2. 이메일과 비밀번호 입력
3. Supabase를 통해 인증
4. 인증 성공 시 대시보드 접근 가능

---

## 2. 시스템 사용자 계정 (Account 모델)

### 용도
- **시스템 내부 권한 관리**
- 역할(role) 기반 접근 제어 (admin, manager, viewer)
- 계정 활성/비활성 상태 관리
- 시스템 내부 기능 접근 권한 제어

### 특징
- ✅ 역할(level) 기반 권한 관리
  - `admin`: 관리자 권한
  - `manager`: 매니저 권한
  - `viewer`: 조회 전용 권한
- ✅ 계정 상태 관리 (`status`: 'Y' 활성, 'N' 비활성)
- ✅ 로컬 데이터베이스(MySQL)에 저장
- ✅ 백엔드 API를 통한 관리

### 저장 위치
- MySQL 데이터베이스의 `Users` 테이블
- 백엔드에서 직접 관리

### 데이터 구조
```python
class Account:
    uqid: int          # 계정 ID
    uid: str           # 사용자명
    uemail: str        # 이메일
    upass: str         # 해시화된 비밀번호
    level: str         # 권한 레벨 (admin/manager/viewer)
    status: str        # 상태 (Y/N)
    last_login: datetime
    regdate: datetime
```

### API 엔드포인트
```
GET    /api/accounts/              # 계정 목록 조회
GET    /api/accounts/<id>          # 특정 계정 조회
POST   /api/accounts/              # 새 계정 생성
PUT    /api/accounts/<id>          # 계정 정보 수정
DELETE /api/accounts/<id>          # 계정 삭제
```

### 사용 위치
```python
# 백엔드
- backend/models/account.py        # Account 모델
- backend/routes/accounts.py       # 계정 관리 API
- frontend/src/pages/Accounts.tsx  # 계정 관리 UI
```

---

## 두 시스템의 관계

### 현재 상태
- **분리된 시스템**: 두 인증 시스템이 독립적으로 작동
- **Supabase**: 웹 앱 접근 인증만 담당
- **Account 모델**: 시스템 내부 권한 관리만 담당

### 연동 필요성
현재는 두 시스템이 연결되어 있지 않습니다. 필요하다면:

1. **Supabase 사용자와 Account 연결**
   - Supabase 사용자의 이메일을 Account의 `uemail`과 매칭
   - 로그인 시 해당 Account의 `level` 정보를 가져와 권한 확인

2. **통합 인증 미들웨어 생성**
   ```python
   # 예시: Supabase 토큰 검증 후 Account 권한 확인
   def verify_user_permission(supabase_user_email):
       account = Account.query.filter_by(uemail=supabase_user_email).first()
       if account and account.status == 'Y':
           return account.level  # admin, manager, viewer
       return None
   ```

---

## 사용 시나리오

### 시나리오 1: 일반 사용자 로그인
1. 사용자가 `/login`에서 Supabase로 로그인
2. 인증 성공 → 대시보드 접근
3. 시스템 기능 사용 시 Account 권한 확인 필요

### 시나리오 2: 관리자가 계정 생성
1. 관리자가 `/accounts` 페이지 접근
2. "새 계정 추가" 클릭
3. Account 모델에 새 계정 생성 (level, status 설정)
4. 해당 사용자는 Supabase에서 별도로 회원가입 필요

### 시나리오 3: 권한 기반 기능 접근
1. 사용자가 특정 기능 접근 시도
2. 백엔드에서 Supabase 토큰 검증
3. 이메일로 Account 조회
4. Account의 `level` 확인하여 권한 부여/거부

---

## 권장 사항

### 옵션 1: 완전 분리 (현재 상태)
- Supabase: 웹 앱 접근 인증
- Account: 시스템 내부 권한 관리
- **장점**: 단순하고 명확한 역할 분리
- **단점**: 두 시스템 동기화 필요

### 옵션 2: 통합 인증
- Supabase 로그인 후 Account 정보 자동 연동
- 이메일을 키로 두 시스템 연결
- **장점**: 일관된 권한 관리
- **단점**: 구현 복잡도 증가

### 옵션 3: Supabase로 완전 전환
- Account 모델 제거
- Supabase의 사용자 메타데이터에 권한 정보 저장
- **장점**: 단일 인증 시스템
- **단점**: 기존 데이터 마이그레이션 필요

---

## 현재 구현 상태

✅ **완료된 작업**
- Supabase 로그인/회원가입 구현
- Account 모델 및 API 유지
- 프론트엔드 인증 컨텍스트 구현

⚠️ **개선 필요**
- 두 시스템 간 연동 로직 없음
- 권한 기반 접근 제어 미구현
- Supabase 사용자와 Account 매핑 없음

---

## 다음 단계

1. **권한 미들웨어 구현**
   - Supabase 토큰 검증
   - Account 권한 확인
   - API 엔드포인트 보호

2. **사용자 연동**
   - Supabase 사용자 이메일과 Account 이메일 매칭
   - 자동 계정 생성 또는 수동 매핑

3. **UI 개선**
   - 현재 로그인한 사용자의 권한 표시
   - 권한에 따른 메뉴/기능 제한

