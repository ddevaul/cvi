import json 
prompt = "plant"
with open(f"voynich_{prompt}_roundness.json", "r") as f:
  voynich = json.load(f)

with open(f"erbario_{prompt}_roundness.json", "r") as f:
  erbario = json.load(f)

erbario.sort(reverse=False, key=lambda e : e['roundness'])

with open(f"tractatus_{prompt}_roundness.json", "r") as f:
  tractatus = json.load(f)

tractatus.sort(reverse=False, key=lambda e : e['roundness'])


def return_closest(roundness: float, compare_arr):
  left = 0
  right = len(compare_arr) - 1
  while left < right:
    mid = (left + right) // 2
    cur_roundness = compare_arr[mid]['roundness']
    if cur_roundness == roundness:
      return compare_arr[mid] 
    if roundness > cur_roundness:
      left = mid + 1
    else:
      right = mid - 1
  return compare_arr[right] 

stuff_to_return = []
for v in voynich:
  closest_erbario = return_closest(v['roundness'], erbario)
  closest_tractatus = return_closest(v['roundness'], tractatus)
  stuff_to_return.append({"voynich": v, "erbario": closest_erbario, "tractatus": closest_tractatus})


with open(f"closest_{prompt}.json", "w") as f:
  json.dump(stuff_to_return, f, indent=2)

  
