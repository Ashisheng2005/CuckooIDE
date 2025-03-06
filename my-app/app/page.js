import * as React from "react"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"


import {
  ModeToggle
} from "@/components/theme-toggle"

import { DirectoryPicker } from "@/components/directory-picker"

// 这里注意要添加一个 default，原本的代码没有这个 default
export default function CardWithForm() {

  return (
    <>
    <div className="flex justify-center items-center h-screen">
    <Card className="w-[600px]">
      <CardHeader>
        
        <CardTitle className="text-2xl"> Create Project</CardTitle>{/* 放大字体:xl--20px, 3xl--30px, 4xl--36px */}
        <CardDescription>Deploy your new project in one-click.</CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="peoject_name">Project Name</Label>
              <Input id="name" placeholder="Name of your project" />
            </div>
            <div className="grid w-full items-center gap-4">
              <Label htmlFor="peoject_path">Project Path</Label>
              <DirectoryPicker/>
            </div>

            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="Project_framework">Peoject Type</Label>
              <Select>
                <SelectTrigger id="Project_framework">
                  <SelectValue placeholder="Mix" />
                </SelectTrigger>
                <SelectContent position="popper">
                  <SelectItem value="Mix">Mix</SelectItem>
                  <SelectItem value="Python">Python</SelectItem>
                  <SelectItem value="C/C++">C/C++</SelectItem>
                  <SelectItem value="Java">Java</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </form>
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button variant="outline">Cancel</Button>
        <Button>Deploy</Button>
      </CardFooter>
    </Card>
    <ModeToggle />
    </div>
    
    </>
  )
}

