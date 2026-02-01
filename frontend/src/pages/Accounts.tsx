import { useState, useEffect, useContext, useCallback } from 'react'
import { Plus, Search, Filter, MoreVertical, Edit, Trash2, Shield, UserCheck, Info, X } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { AuthContext } from '../context/AuthContext'

interface AccountType {
  uqid: number;
  uid: string;
  uname?: string;
  name?: string;
  uemail: string;
  level: 'admin' | 'manager' | 'viewer';
  status: 'Y' | 'N';
  last_login: string;
  regdate: string;
}

const Accounts = () => {
  const [showHelp, setShowHelp] = useState(false)
  const authContext = useContext(AuthContext);

  if (!authContext) {
    throw new Error('AuthContext must be used within an AuthProvider');
  }

  const { session, logout } = authContext;

  const [accounts, setAccounts] = useState<AccountType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  const [showAddAccountModal, setShowAddAccountModal] = useState(false);
  const [showEditAccountModal, setShowEditAccountModal] = useState(false);
  
  const [newAccount, setNewAccount] = useState({
    uid: '',
    uemail: '',
    password: '',
    level: 'viewer' as AccountType['level'],
    uname: '',
  });

  const [editingAccount, setEditingAccount] = useState<any>(null);
  
  const [addAccountLoading, setAddAccountLoading] = useState(false);
  const [addAccountError, setAddAccountError] = useState<string | null>(null);

  const [updateAccountLoading, setUpdateAccountLoading] = useState(false);
  const [updateAccountError, setUpdateAccountError] = useState<string | null>(null);

  const [searchTerm, setSearchTerm] = useState('');

  const fetchAccounts = useCallback(async () => {
    if (!session || !session.access_token) {
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/accounts/', {
        headers: {
          'Authorization': `Bearer ${session.access_token}`
        }
      });
      if (response.status === 401) {
        alert('인증 세션이 만료되었습니다. 다시 로그인해주세요.');
        logout();
        return;
      }
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      
      const fetchedAccounts: AccountType[] = data.accounts.map((acc: any) => ({
        uqid: acc.uqid,
        uid: acc.uid,
        uname: acc.name, // backend to_dict returns 'name' for uname
        uemail: acc.uemail,
        level: acc.level,
        status: acc.status,
        last_login: acc.last_login || 'N/A',
        regdate: acc.regdate,
      }));
      setAccounts(fetchedAccounts);
    } catch (e: any) {
      setError(`계정 목록을 불러오는데 실패했습니다: ${e.message}`);
      console.error("Failed to fetch accounts:", e);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

  const handleAddAccountSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAddAccountLoading(true);
    setAddAccountError(null);

    if (!session || !session.access_token) {
      setAddAccountError('인증 정보가 없습니다. 다시 로그인해주세요.');
      setAddAccountLoading(false);
      return;
    }

    try {
      const response = await fetch('/api/accounts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`,
        },
        body: JSON.stringify(newAccount),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || '계정 추가에 실패했습니다.');
      }

      alert('계정이 성공적으로 추가되었습니다.');
      setShowAddAccountModal(false);
      setNewAccount({
        uid: '',
        uemail: '',
        password: '',
        level: 'viewer',
        uname: '',
      });
      fetchAccounts();
    } catch (e: any) {
      console.error("Failed to add account:", e);
      setAddAccountError(e.message || '알 수 없는 오류가 발생했습니다.');
    } finally {
      setAddAccountLoading(false);
    }
  };

  const handleEditClick = (account: AccountType) => {
    setEditingAccount({
      uqid: account.uqid,
      uid: account.uid,
      uname: account.uname || '',
      uemail: account.uemail,
      level: account.level,
      status: account.status,
      password: '', // Password empty by default when editing
    });
    setShowEditAccountModal(true);
  };

  const handleUpdateAccountSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setUpdateAccountLoading(true);
    setUpdateAccountError(null);

    if (!session || !session.access_token) {
      setUpdateAccountError('인증 정보가 없습니다. 다시 로그인해주세요.');
      setUpdateAccountLoading(false);
      return;
    }

    try {
      const response = await fetch(`/api/accounts/${editingAccount.uqid}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`,
        },
        body: JSON.stringify(editingAccount),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || '계정 수정에 실패했습니다.');
      }

      alert('계정 정보가 성공적으로 수정되었습니다.');
      setShowEditAccountModal(false);
      fetchAccounts();
    } catch (e: any) {
      console.error("Failed to update account:", e);
      setUpdateAccountError(e.message || '알 수 없는 오류가 발생했습니다.');
    } finally {
      setUpdateAccountLoading(false);
    }
  };

  const handleDeleteAccount = async (account: AccountType) => {
    if (!window.confirm(`'${account.uid}' 계정을 삭제하시겠습니까?`)) {
      return;
    }

    if (!session || !session.access_token) {
      alert('인증 정보가 없습니다. 다시 로그인해주세요.');
      return;
    }

    try {
      const response = await fetch(`/api/accounts/${account.uqid}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${session.access_token}`,
        },
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || '계정 삭제에 실패했습니다.');
      }

      alert('계정이 삭제되었습니다.');
      fetchAccounts();
    } catch (e: any) {
      console.error("Failed to delete account:", e);
      alert(e.message || '알 수 없는 오류가 발생했습니다.');
    }
  };

  const getRoleColor = (level: string) => {
    switch (level) {
      case 'admin': return 'from-red-500 to-pink-500'
      case 'manager': return 'from-blue-500 to-cyan-500'
      case 'viewer': return 'from-green-500 to-emerald-500'
      default: return 'from-gray-500 to-gray-700'
    }
  }

  const getRoleLabel = (level: string) => {
    switch (level) {
      case 'admin': return '관리자'
      case 'manager': return '매니저'
      case 'viewer': return '뷰어'
      default: return level
    }
  }

  const filteredAccounts = accounts.filter(account => 
    account.uid.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (account.uname && account.uname.toLowerCase().includes(searchTerm.toLowerCase())) ||
    account.uemail.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div>
            <h1 className="text-3xl font-bold gradient-text mb-2">계정 관리</h1>
            <p className="text-muted-foreground">시스템 사용자 계정을 관리하세요</p>
          </div>
          <div className="relative">
            <button
              onClick={() => setShowHelp(!showHelp)}
              className={`group relative p-3 rounded-xl transition-all duration-200 ${
                showHelp
                  ? 'bg-primary/20 text-primary border-2 border-primary shadow-lg shadow-primary/20 scale-105'
                  : 'bg-blue-500/10 text-blue-500 border-2 border-blue-500/30 hover:bg-blue-500/20 hover:border-blue-500/50 hover:scale-105 shadow-md'
              }`}
              title="권한 레벨 도움말"
            >
              <Info className="w-5 h-5" />
              {showHelp && (
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-primary rounded-full animate-pulse"></span>
              )}
            </button>
            {!showHelp && (
              <span className="absolute -top-1 -right-1 w-2 h-2 bg-blue-500 rounded-full animate-ping"></span>
            )}
          </div>
        </div>
        <button
          onClick={() => setShowAddAccountModal(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>새 계정 추가</span>
        </button>
      </div>

      {/* 권한 레벨 도움말 */}
      {showHelp && (
        <Card className="glass rounded-2xl border-primary/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
            <CardTitle className="text-lg font-semibold flex items-center space-x-2">
              <Info className="w-5 h-5 text-primary" />
              <span>권한 레벨 안내</span>
            </CardTitle>
            <button
              onClick={() => setShowHelp(false)}
              className="p-1 text-muted-foreground hover:text-foreground transition-colors rounded-lg hover:bg-muted/50"
            >
              <X className="w-4 h-4" />
            </button>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-start space-x-3 p-3 rounded-lg bg-gradient-to-r from-red-500/10 to-pink-500/10 border border-red-500/20">
                <Shield className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="font-semibold text-red-500">admin</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-red-500/20 text-red-500">관리자</span>
                  </div>
                  <p className="text-sm text-muted-foreground">모든 권한 (생성, 수정, 삭제)</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3 p-3 rounded-lg bg-gradient-to-r from-blue-500/10 to-cyan-500/10 border border-blue-500/20">
                <UserCheck className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="font-semibold text-blue-500">manager</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-500">매니저</span>
                  </div>
                  <p className="text-sm text-muted-foreground">생성, 수정 권한</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3 p-3 rounded-lg bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/20">
                <UserCheck className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="font-semibold text-green-500">viewer</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-green-500/20 text-green-500">뷰어</span>
                  </div>
                  <p className="text-sm text-muted-foreground">조회 전용 권한</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
      
      {/* 검색 및 필터 */}
      <div className="glass rounded-2xl p-6">
        <div className="flex items-center space-x-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <input
              type="text"
              placeholder="계정 검색..."
              className="w-full pl-10 pr-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 border border-border rounded-xl hover:bg-muted/50 transition-colors">
            <Filter className="w-4 h-4" />
            <span>필터</span>
          </button>
        </div>
      </div>
      
      {/* 계정 목록 */}
      <div className="glass rounded-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-border">
              <tr>
                <th className="text-left p-6 font-medium text-muted-foreground">사용자</th>
                <th className="text-left p-6 font-medium text-muted-foreground">이름</th>
                <th className="text-left p-6 font-medium text-muted-foreground">이메일</th>
                <th className="text-left p-6 font-medium text-muted-foreground">역할</th>
                <th className="text-left p-6 font-medium text-muted-foreground">상태</th>
                <th className="text-left p-6 font-medium text-muted-foreground">마지막 로그인</th>
                <th className="text-right p-6 font-medium text-muted-foreground">액션</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={7} className="text-center p-6 text-muted-foreground">계정 목록을 불러오는 중...</td>
                </tr>
              ) : error ? (
                <tr>
                  <td colSpan={7} className="text-center p-6 text-red-500">{error}</td>
                </tr>
              ) : filteredAccounts.length === 0 ? (
                <tr>
                  <td colSpan={7} className="text-center p-6 text-muted-foreground">표시할 계정이 없습니다.</td>
                </tr>
              ) : (
                filteredAccounts.map((account) => (
                  <tr key={account.uqid} className="border-b border-border/50 hover:bg-muted/30 transition-colors">
                    <td className="p-6">
                      <div className="flex items-center space-x-3">
                        <div className={`w-10 h-10 bg-gradient-to-r ${getRoleColor(account.level)} rounded-xl flex items-center justify-center`}>
                          {account.level === 'admin' ? (
                            <Shield className="w-5 h-5 text-white" />
                          ) : (
                            <UserCheck className="w-5 h-5 text-white" />
                          )}
                        </div>
                        <div>
                          <p className="font-medium">{account.uid}</p>
                        </div>
                      </div>
                    </td>
                    <td className="p-6">
                      <span className="text-sm">{account.uname}</span>
                    </td>
                    <td className="p-6">
                      <span className="text-sm">{account.uemail}</span>
                    </td>
                    <td className="p-6">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium bg-gradient-to-r ${getRoleColor(account.level)} text-white`}>
                        {getRoleLabel(account.level)}
                      </span>
                    </td>
                    <td className="p-6">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        account.status === 'Y' 
                          ? 'bg-green-500/20 text-green-500' 
                          : 'bg-red-500/20 text-red-500'
                      }`}>
                        {account.status === 'Y' ? '활성' : '비활성'}
                      </span>
                    </td>
                    <td className="p-6">
                      <span className="text-sm text-muted-foreground">{account.last_login !== 'N/A' ? new Date(account.last_login).toLocaleString() : 'N/A'}</span>
                    </td>
                    <td className="p-6">
                      <div className="flex items-center justify-end space-x-2">
                        <button 
                          onClick={() => handleEditClick(account)}
                          className="p-2 text-muted-foreground hover:text-foreground transition-colors"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button 
                          onClick={() => handleDeleteAccount(account)}
                          className="p-2 text-muted-foreground hover:text-red-500 transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                        <button className="p-2 text-muted-foreground hover:text-foreground transition-colors">
                          <MoreVertical className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
      
      {/* Add New Account Modal */}
      {showAddAccountModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="glass rounded-2xl p-8 w-full max-w-md mx-auto">
            <h2 className="text-2xl font-bold mb-6 text-primary-foreground">새 계정 추가</h2>
            <form onSubmit={handleAddAccountSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1" htmlFor="add-uid">
                  사용자명 (ID)
                </label>
                <input
                  type="text"
                  id="add-uid"
                  className="w-full px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                  value={newAccount.uid}
                  onChange={(e) => setNewAccount({ ...newAccount, uid: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1" htmlFor="add-uemail">
                  이메일
                </label>
                <input
                  type="email"
                  id="add-uemail"
                  className="w-full px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                  value={newAccount.uemail}
                  onChange={(e) => setNewAccount({ ...newAccount, uemail: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1" htmlFor="add-uname">
                  이름 (Name)
                </label>
                <input
                  type="text"
                  id="add-uname"
                  className="w-full px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                  value={newAccount.uname}
                  onChange={(e) => setNewAccount({ ...newAccount, uname: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1" htmlFor="add-password">
                  비밀번호
                </label>
                <input
                  type="password"
                  id="add-password"
                  className="w-full px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                  value={newAccount.password}
                  onChange={(e) => setNewAccount({ ...newAccount, password: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1" htmlFor="add-level">
                  역할
                </label>
                <select
                  id="add-level"
                  className="w-full px-4 py-2 bg-slate-800 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                  value={newAccount.level}
                  onChange={(e) => setNewAccount({ ...newAccount, level: e.target.value as AccountType['level'] })}
                  required
                >
                  <option value="viewer">뷰어</option>
                  <option value="manager">매니저</option>
                  <option value="admin">관리자</option>
                </select>
              </div>
              {addAccountError && (
                <p className="text-red-500 text-sm mt-2">{addAccountError}</p>
              )}
              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => setShowAddAccountModal(false)}
                  className="px-4 py-2 rounded-xl text-muted-foreground hover:bg-muted/50 transition-colors"
                >
                  취소
                </button>
                <button
                  type="submit"
                  disabled={addAccountLoading}
                  className="px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-colors disabled:opacity-50"
                >
                  {addAccountLoading ? '추가 중...' : '계정 추가'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Account Modal */}
      {showEditAccountModal && editingAccount && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="glass rounded-2xl p-8 w-full max-w-md mx-auto">
            <h2 className="text-2xl font-bold mb-6 text-primary-foreground">계정 정보 수정</h2>
            <form onSubmit={handleUpdateAccountSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1" htmlFor="edit-uid">
                  사용자명 (ID)
                </label>
                <input
                  type="text"
                  id="edit-uid"
                  className="w-full px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                  value={editingAccount.uid}
                  onChange={(e) => setEditingAccount({ ...editingAccount, uid: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1" htmlFor="edit-uemail">
                  이메일
                </label>
                <input
                  type="email"
                  id="edit-uemail"
                  className="w-full px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                  value={editingAccount.uemail}
                  onChange={(e) => setEditingAccount({ ...editingAccount, uemail: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1" htmlFor="edit-uname">
                  이름 (Name)
                </label>
                <input
                  type="text"
                  id="edit-uname"
                  className="w-full px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                  value={editingAccount.uname}
                  onChange={(e) => setEditingAccount({ ...editingAccount, uname: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1" htmlFor="edit-password">
                  비밀번호 (변경할 경우만 입력)
                </label>
                <input
                  type="password"
                  id="edit-password"
                  className="w-full px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                  value={editingAccount.password}
                  onChange={(e) => setEditingAccount({ ...editingAccount, password: e.target.value })}
                  placeholder="새 비밀번호"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-1" htmlFor="edit-level">
                    역할
                  </label>
                  <select
                    id="edit-level"
                    className="w-full px-4 py-2 bg-slate-800 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                    value={editingAccount.level}
                    onChange={(e) => setEditingAccount({ ...editingAccount, level: e.target.value as AccountType['level'] })}
                    required
                  >
                    <option value="viewer">뷰어</option>
                    <option value="manager">매니저</option>
                    <option value="admin">관리자</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-1" htmlFor="edit-status">
                    상태
                  </label>
                  <select
                    id="edit-status"
                    className="w-full px-4 py-2 bg-slate-800 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                    value={editingAccount.status}
                    onChange={(e) => setEditingAccount({ ...editingAccount, status: e.target.value as 'Y' | 'N' })}
                    required
                  >
                    <option value="Y">활성</option>
                    <option value="N">비활성</option>
                  </select>
                </div>
              </div>
              {updateAccountError && (
                <p className="text-red-500 text-sm mt-2">{updateAccountError}</p>
              )}
              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => setShowEditAccountModal(false)}
                  className="px-4 py-2 rounded-xl text-muted-foreground hover:bg-muted/50 transition-colors"
                >
                  취소
                </button>
                <button
                  type="submit"
                  disabled={updateAccountLoading}
                  className="px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-colors disabled:opacity-50"
                >
                  {updateAccountLoading ? '수정 중...' : '정보 수정'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Accounts
