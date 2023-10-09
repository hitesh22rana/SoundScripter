import Wrapper from "@/src/components/dashboard/Wrapper";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return <Wrapper>{children}</Wrapper>;
}
