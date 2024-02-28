import screen_analysis_module as sam
from window_module import get_scale_factor

scale_factor = get_scale_factor()

result = sam.get_window_title_coord('блокнот', scale_factor=1.0)

print(result)

