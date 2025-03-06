"use client"; // 标记为 Client Component

import React, { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { FolderIcon } from "lucide-react"; // 使用 Lucide 图标库

export function DirectoryPicker() {
  const [value, setValue] = useState("");
  const [isClient, setIsClient] = useState(false); // 用于检测是否在客户端
  const inputRef = useRef<HTMLInputElement>(null);

  // 在组件挂载后标记为客户端
  useEffect(() => {
    setIsClient(true);
  }, []);

  // 处理文件夹选择
  const handleDirectoryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      // 获取文件夹路径
      const path = files[0].webkitRelativePath;
      setValue(path);
    }
  };

  // 直接触发 input 的点击事件
  const handleButtonClick = () => {
    if (inputRef.current) {
      inputRef.current.click();
    }
  };

  return (
    <div className="space-y-4">
      {/* 输入框和按钮组合 */}
      <div className="flex items-center gap-2">
        <Input
          value={value}
          type="text"
          className="flex-1"
          readOnly // 输入框只读
          placeholder="Select your project path"
        />
        {/* 只在客户端渲染文件选择输入框 */}
        {isClient && (
          <>
            <input
              type="file"
              id="directoryPicker"
              ref={inputRef}
              // @ts-ignore - webkitdirectory 是浏览器特有的属性
              webkitdirectory="true" // 允许选择文件夹
              onChange={handleDirectoryChange}
              // style={{ opacity: 0, position: "absolute", zIndex: -1 }} // 隐藏但不阻止事件
            />
            {/* 触发文件选择的按钮 */}
            <Button
              variant="outline"
              size="icon" // 按钮为图标大小
              className="w-10 h-10 rounded-lg" // 圆角正方形
              onClick={handleButtonClick} // 直接触发 input 点击
            >
              <FolderIcon className="h-5 w-5" /> {/* 使用文件夹图标 */}
            </Button>
          </>
        )}
      </div>
    </div>
  );
}

export default DirectoryPicker;