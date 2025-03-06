import { Button, Card, Typography } from "shadcn-ui";

const YourPage = () => {
  return (
    <div className="container mx-auto p-4">
      <Typography variant="h1">欢迎来到 YourPage 页面</Typography>
      <Card className="mt-4 p-4">
        <Typography variant="p">这里是页面的内容部分</Typography>
        <Button className="mt-2">点击我</Button>
      </Card>
    </div>
  );
};

export default YourPage;