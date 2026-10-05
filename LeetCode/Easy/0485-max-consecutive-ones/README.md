# Max Consecutive Ones

- Platform: LeetCode
- Difficulty: Easy
- Topic: Array

# 🔢 Max Consecutive Ones

**LeetCode:** 485 — Max Consecutive Ones  
**Topic:** Array | Traversal | Counting  
**Difficulty:** Easy

---

## 📌 Problem

Given a binary array `nums`, find the maximum number of consecutive `1`s.

```text
Input:  [1,1,0,1,1,1]
Output: 3
```

---

# 1️⃣ Approach 1 — Store Every Streak

### 💡 Idea

- Traverse the array.
- When `1` is found, count consecutive `1`s using a `while` loop.
- Store each streak in `Counts`.
- Find the maximum using `max_element()`.

### Code

```cpp
class Solution {
public:
    int findMaxConsecutiveOnes(vector<int>& nums) {

        vector<int> Counts;

        for(int i = 0; i < nums.size(); i++) {

            if(nums[i] == 1) {

                int count = 0;

                while(i < nums.size() && nums[i] != 0) {
                    count++;
                    i++;
                }

                Counts.push_back(count);
            }
        }

        if(Counts.empty()) {
            return 0;
        }

        return *max_element(Counts.begin(), Counts.end());
    }
};
```

### ⚠️ Issues

- `Counts` stores all streaks, but we only need the maximum.
- Extra `vector` → **O(n) space**.
- `max_element()` requires finding the maximum afterward.

### Complexity

**Time:** `O(n)`  
**Space:** `O(n)`

---

# 2️⃣ Approach 2 — Track Maximum Directly

### 💡 What Changed?

Removed the unnecessary `Counts` vector.

Instead of:

```cpp
Counts.push_back(count);
```

directly update the maximum:

```cpp
if(count > max) {
    max = count;
}
```

### Code

```cpp
class Solution {
public:
    int findMaxConsecutiveOnes(vector<int>& nums) {

        if(vector.size() == 0) {
            return 0;
        }

        int max = 0;

        for(int i = 0; i < nums.size(); i++) {

            if(nums[i] == 1) {

                int count = 0;

                while(i < nums.size() && nums[i] != 0) {
                    count++;
                    i++;
                }

                if(count > max) {
                    max = count;
                }
            }
        }

        return max;
    }
};
```

### ⚠️ Mistake

```cpp
vector.size()
```

is incorrect. It should be:

```cpp
nums.size()
```

But the empty-array check isn't necessary anyway because `max` starts at `0`.

### ✅ Improvement

```text
Approach 1 → Store all streaks → O(n) space
Approach 2 → Store only maximum → O(1) space
```

### Complexity

**Time:** `O(n)`  
**Space:** `O(1)`

---

# 3️⃣ Approach 3 — Running Counter ⭐

### 💡 Key Idea

Instead of using a separate `while` loop for every streak, maintain the current streak while traversing.

Use two variables:

- `count` → current consecutive `1`s
- `maxi` → maximum streak found so far

### Logic

If the element is `1`:

```cpp
count++;
maxi = max(maxi, count);
```

If the element is `0`:

```cpp
count = 0;
```

### Code

```cpp
class Solution {
public:
    int findMaxConsecutiveOnes(vector<int>& nums) {

        int maxi = 0;
        int count = 0;

        for(int i = 0; i < nums.size(); i++) {

            if(nums[i] == 1) {
                count++;
                maxi = max(maxi, count);
            }
            else {
                count = 0;
            }
        }

        return maxi;
    }
};
```

---

# 🔄 Solution Evolution

```text
Approach 1
Count → Store every streak → Find maximum
                ↓
        Unnecessary storage

Approach 2
Count → Update maximum directly
                ↓
        O(1) space

Approach 3
Running count + maximum
                ↓
        Simpler one-pass solution
```

---

# ⭐ Key Improvements

### 1. Remove unnecessary storage

If we only need the maximum, don't store every value.

### 2. Maintain the current state

`count` tells us how many consecutive `1`s we currently have.

### 3. Reset when the sequence breaks

```cpp
count = 0;
```

when we encounter `0`.

### 4. Update the answer immediately

```cpp
maxi = max(maxi, count);
```

No need for another pass.

---

# 📊 Complexity

| Approach | Time | Space |
|---|---|---|
| Approach 1 | O(n) | O(n) |
| Approach 2 | O(n) | O(1) |
| Approach 3 | O(n) | O(1) |

---

# 🧠 Key Takeaway

The main learning from this problem:

```text
Store everything
      ↓
Store only what matters
      ↓
Maintain the answer while traversing
```

For **consecutive/streak problems**, remember this pattern:

```cpp
if(condition) {
    count++;
    answer = max(answer, count);
}
else {
    count = 0;
}
```

**Final solution:** `O(n)` time and `O(1)` space.