export function isLoggedIn() {
    return !!localStorage.user
}
  
  
export function getCurrentUser() {
    return localStorage.user;
}