import { Flex, Spinner, Text } from "@radix-ui/themes";

export function LoadingSpinner({ label = "Loading..." }: { label?: string }) {
  return (
    <Flex align="center" justify="center" py="9" gap="3">
      <Spinner size="3" />
      <Text size="3" color="gray">
        {label}
      </Text>
    </Flex>
  );
}
