import instaloader
import sys
import time

def get_profile_data(username, max_retries=3, retry_delay=60):
    bot = instaloader.Instaloader()
    # 로그인 세션 사용 (쿠키 파일 또는 직접 로그인)
    try:
        #bot.login('your_username', 'your_password') # Instagram 계정 로그인
        #bot.load_session_from_file('your_username') # 세션 파일 사용 시 활성화
        pass
    except Exception as e:
        print(f"[Error] Instagram 로그인 실패: {e}", file=sys.stderr)
        return None

    for attempt in range(max_retries):
        try:
            profile = instaloader.Profile.from_username(bot.context, username)
            return profile
        except instaloader.exceptions.ConnectionException as e:
            error_str = str(e)
            if "401 Unauthorized" in error_str or "429 Too Many Requests" in error_str:
                if attempt < max_retries - 1:
                    print(f"[Warning] {error_str} for user '{username}'. Attempt {attempt+1}/{max_retries}. Waiting {retry_delay} seconds before retrying...")
                    time.sleep(retry_delay)
                else:
                    print(f"[Error] {error_str} persists after {max_retries} attempts. Exiting.", file=sys.stderr)
                    return None
            else:
                print(f"[Error] Failed to get profile for {username}: {error_str}", file=sys.stderr)
                return None
        except instaloader.exceptions.ProfileNotExistsException:
            print(f"[Error] The user '{username}' does not exist.", file=sys.stderr)
            return None
        except Exception as ex:
            print(f"[Error] Unexpected error: {ex}", file=sys.stderr)
            return None
    return None

if __name__ == "__main__":
    Username = 'zankke'
    profile = get_profile_data(Username)
    if profile:
        print("Username:", profile.username)
        print("User ID:", profile.userid)
        print("Number of Posts:", profile.mediacount)
        print("Followers:", profile.followers)
        print("Followees:", profile.followees)
        print("Bio:", profile.biography, profile.external_url)
    else:
        print(f"Could not retrieve profile information for '{Username}'.")
