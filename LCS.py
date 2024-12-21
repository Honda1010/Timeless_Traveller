
dp = {}
x = "abcs"
y="acs"
ans = ""
def lcs(i, j):
    if i >= len(x) or y >= len(y):
        return 0
    if dp[i][j] is not -1:
        return dp[i][j]
    if x[i] == y[j]:
        return lcs(i + 1, j + 1) + 1
    dp[i][j] = max(lcs(i + 1, j), lcs(i, j + 1))
    return dp[i][j]

def build(i, j):
    if i >= len(x) or j >= len(y):
        return 0
    if(x[i] == y[j]):
        ans += x[i]
        return build(i + 1, j + 1)
    if lcs(i + 1, j) == lcs(i,j):
        return build(i + 1, j)
    return build(i, j + 1)
    