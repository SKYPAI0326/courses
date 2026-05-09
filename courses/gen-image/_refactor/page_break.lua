-- 把帶 class="page-break" 的 <hr> 或 <div> 轉成 Word 真正分頁符。
-- 其他 hr 維持原樣（裝飾用水平線）。

local PAGE_BREAK_OOXML = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

function has_pb(attr)
  if not attr or not attr.classes then return false end
  for _, c in ipairs(attr.classes) do
    if c == "page-break" then return true end
  end
  return false
end

function HorizontalRule(elem)
  if FORMAT:match("docx") and has_pb(elem.attr) then
    return pandoc.RawBlock("openxml", PAGE_BREAK_OOXML)
  end
end

function Div(elem)
  if FORMAT:match("docx") and has_pb(elem.attr) then
    return pandoc.RawBlock("openxml", PAGE_BREAK_OOXML)
  end
end
