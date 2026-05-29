function Pandoc(doc)
  local blocks = {}
  local i = 1
  while i <= #doc.blocks do
    local b = doc.blocks[i]
    if b.t == "RawBlock" and b.format == "tex" then
      -- merge consecutive RawBlocks
      local lines = {b.text}
      i = i + 1
      while i <= #doc.blocks and doc.blocks[i].t == "RawBlock" and doc.blocks[i].format == "tex" do
        table.insert(lines, doc.blocks[i].text)
        i = i + 1
      end
      table.insert(blocks, pandoc.RawBlock("tex", table.concat(lines, "\n")))
    else
      table.insert(blocks, b)
      i = i + 1
    end
  end
  doc.blocks = blocks
  return doc
end
