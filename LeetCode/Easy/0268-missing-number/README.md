# 🔢 Missing Number

**LeetCode:** 268 — Missing Number  
**Topic:** Array | Math | XOR  
**Difficulty:** Easy

---

## 📌 Problem

Given an array containing `n` distinct numbers from `0` to `n`, find the one missing number.

### Example

```text
Input:  [3,0,1]
Output: 2
```

The complete range is:

```text
0 1 2 3
    ↑
  Missing
```

---

# 1️⃣ Approach 1 — Brute Force

### 💡 Idea

For every number from `0` to `n`:

1. Search for that number in the array.
2. If it doesn't exist, return it.

### Code

```cpp
class Solution {
public:
    int missingNumber(vector<int>& nums) {

        int n = nums.size();

        for(int i = 0; i <= n; i++) {

            bool found = false;

            for(int j = 0; j < n; j++) {

                if(nums[j] == i) {
                    found = true;
                    break;
                }
            }

            if(!found) {
                return i;
            }
        }

        return -1;
    }
};
```

### ⚠️ Problem

For every number, we search the entire array.

This creates a nested loop.

### Complexity

**Time:** `O(n²)`  
**Space:** `O(1)`

---

# 2️⃣ Approach 2 — Buffer / Extra Space

### 💡 Idea

Use an extra array to mark which numbers are present.

```text
nums = [3,0,1]

Present:
0 → ✓
1 → ✓
2 → ✗
3 → ✓
```

### Code

```cpp
class Solution {
public:
    int missingNumber(vector<int>& nums) {

        int n = nums.size();

        vector<bool> present(n + 1, false);

        for(int num : nums) {
            present[num] = true;
        }

        for(int i = 0; i <= n; i++) {

            if(!present[i]) {
                return i;
            }
        }

        return -1;
    }
};
```

### ✅ Improvement

Instead of searching the array repeatedly, we directly mark each number as present.

### ⚠️ Problem

We use an additional array.

### Complexity

**Time:** `O(n)`  
**Space:** `O(n)`

---

# 3️⃣ Approach 3 — Sum Formula ⭐

### 💡 Idea

The numbers should contain:

```text
0 + 1 + 2 + ... + n
```

The sum of `0` to `n` is:

```text
n(n + 1) / 2
```

So:

```text
Missing Number = Expected Sum - Actual Sum
```

### Example

```text
nums = [3,0,1]
n = 3

Expected Sum = 3 × 4 / 2
              = 6

Actual Sum = 3 + 0 + 1
           = 4

Missing = 6 - 4
        = 2
```

### Code

```cpp
class Solution {
public:
    int missingNumber(vector<int>& nums) {

        int n = nums.size();

        int totalSum = (n * (n + 1)) / 2;

        int sum = 0;

        for(int i = 0; i < n; i++) {
            sum += nums[i];
        }

        return totalSum - sum;
    }
};
```

### ✅ Improvement

- No extra array.
- Only one traversal.
- Very simple mathematical solution.

### Complexity

**Time:** `O(n)`  
**Space:** `O(1)`

---

# 4️⃣ Approach 4 — XOR ⭐

### 💡 Idea

Use the XOR properties:

```text
a ^ a = 0
a ^ 0 = a
```

If we XOR all numbers from `0` to `n` with all numbers in the array, every existing number cancels out.

Only the missing number remains.

### Example

```text
nums = [3,0,1]

Expected:
0 ^ 1 ^ 2 ^ 3

Array:
3 ^ 0 ^ 1

Combined:

0 ^ 1 ^ 2 ^ 3
^ 3 ^ 0 ^ 1
--------------
2
```

Everything appears twice except `2`.

### Code

```cpp
class Solution {
public:
    int missingNumber(vector<int>& nums) {

        int n = nums.size();

        int xor1 = 0;
        int xor2 = 0;

        for(int i = 0; i <= n - 1; i++) {

            xor2 = xor2 ^ nums[i];
            xor1 = xor1 ^ (i + 1);
        }

        return xor1 ^ xor2;
    }
};
```

### Why `i + 1`?

The loop runs from:

```text
i = 0 → n-1
```

So:

```text
i + 1 = 1 → n
```

Since `xor1` starts at `0`, it already includes `0`.

Therefore it effectively calculates:

```text
0 ^ 1 ^ 2 ^ ... ^ n
```

---

# 🔄 Solution Evolution

```text
Approach 1 — Brute Force
O(n²) time, O(1) space
        ↓
Remove repeated searching

Approach 2 — Buffer
O(n) time, O(n) space
        ↓
Remove extra storage

Approach 3 — Sum Formula
O(n) time, O(1) space
        ↓
Mathematical solution

Approach 4 — XOR
O(n) time, O(1) space
        ↓
Bit manipulation solution
```

---

# 📊 Complexity Comparison

| Approach | Technique | Time | Space |
|---|---|---:|---:|
| 1 | Brute Force | O(n²) | O(1) |
| 2 | Buffer | O(n) | O(n) |
| 3 | Sum Formula | O(n) | O(1) |
| 4 | XOR | O(n) | O(1) |

---

# ⭐ Key Highlights

### Brute Force

> Search every possible number in the array.

Main problem: **Repeated searching → O(n²)**

---

### Buffer

> Store whether each number exists.

Main problem: **Extra O(n) memory**

---

### Sum

> Expected sum − Actual sum = Missing number.

```cpp
(n * (n + 1)) / 2
```

**O(n) time + O(1) space**

---

### XOR

> Duplicate numbers cancel each other.

```cpp
x ^ x = 0
```

The missing number remains.

**O(n) time + O(1) space**

---

# 🧠 Final Learning

This problem teaches an important optimization progression:

```text
Brute Force
    ↓
Use Extra Data Structure
    ↓
Use Mathematical Property
    ↓
Use Bit Manipulation
```

The two optimal solutions are:

### 🧮 Sum

Easy to understand using mathematics.

### ⚡ XOR

Avoids sum calculation and uses the cancellation property of XOR.

Both achieve:

```text
Time  → O(n)
Space → O(1)
```

**Key DSA pattern:** Before using extra memory, look for a **mathematical or bitwise property** that can eliminate it.