-- build/chapter-headings.lua
--
-- 1. For top-level headings of the form "Chapter N. Title" or "Appendix A. Title",
--    insert a line break after the period so the heading renders on two lines in
--    both HTML and LaTeX.
-- 2. In LaTeX output, restart footnote numbering at every top-level heading, so
--    each chapter's notes are numbered from 1. (Chapter headings are unnumbered
--    in pandoc's LaTeX output, so LaTeX's own chapter counter never resets them.)
-- 3. A ::: {.center} ::: div centers its content. Pandoc's LaTeX writer does not
--    do this on its own for an uncaptioned image (only a captioned figure gets
--    \centering), so in LaTeX output this wraps the content in \begin{center}.
--    In HTML the div passes through and site-extra.css centers it.

local function is_chapter_marker(elements)
  if #elements < 3 then return false end
  local first, second, third = elements[1], elements[2], elements[3]
  if first.t ~= "Str" then return false end
  if first.text ~= "Chapter" and first.text ~= "Appendix" then return false end
  if second.t ~= "Space" then return false end
  if third.t ~= "Str" then return false end
  return string.match(third.text, "^%d+%.$") or
         string.match(third.text, "^%u%.$")
end

function Header(elem)
  if elem.level ~= 1 then return nil end

  if is_chapter_marker(elem.content) then
    -- Keep "Chapter", space, "N.", then a line break, drop the following space,
    -- and keep the rest of the title.
    local new = {}
    for i = 1, 3 do new[#new + 1] = elem.content[i] end
    new[#new + 1] = pandoc.LineBreak()
    for i = 5, #elem.content do new[#new + 1] = elem.content[i] end
    elem.content = new
  end

  if FORMAT:match("latex") or FORMAT:match("pdf") then
    return { pandoc.RawBlock("latex", "\\setcounter{footnote}{0}"), elem }
  end
  return elem
end

function Div(elem)
  if not elem.classes:includes("center") then return nil end
  if FORMAT:match("latex") or FORMAT:match("pdf") then
    local blocks = { pandoc.RawBlock("latex", "\\begin{center}") }
    for _, b in ipairs(elem.content) do blocks[#blocks + 1] = b end
    blocks[#blocks + 1] = pandoc.RawBlock("latex", "\\end{center}")
    return blocks
  end
  return nil
end
